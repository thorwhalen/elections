"""New York Times Election Data Source

This module provides access to election data from the New York Times' unofficial
election results API. The API provides detailed election results including vote
counts, candidate information, and time-series data for U.S. elections.

**Data Source:** New York Times Elections Assets API (unofficial)
**URL Pattern:** https://static01.nyt.com/elections-assets/{year}/data/api/{date}/...
**Access:** Free, no API key required
**Coverage:** U.S. presidential and other races for 2016, 2020, 2024
**Data Types:** Election results, vote counts, time-series data, race details

**More Information:**
- Example usage: https://gist.github.com/curran/b218499a412033064fea7936334b86bb
- Background: https://source.opennews.org/articles/ny-times-results-loader/

**Note:** This is an unofficial API that powers the NYT election website. The API
structure has been consistent across election years but is not officially documented
or guaranteed to remain available.

**Example Usage:**

    >>> from elections.nytimes import get_election_data, get_races, get_president_timeseries  # doctest: +SKIP
    >>>
    >>> # Get raw election data for Pennsylvania in 2020
    >>> data = get_election_data(region='pennsylvania', year=2020)  # doctest: +SKIP
    >>>
    >>> # Get races for a specific state
    >>> races = get_races(region='florida', year=2024)  # doctest: +SKIP
    >>>
    >>> # Get president race time series
    >>> timeseries = get_president_timeseries(region='georgia', year=2020)  # doctest: +SKIP

"""

from functools import partial
from typing import Dict, List, Optional, Any
from datetime import date as date_type

import requests
import pandas as pd

from py2store.utils.explicit import ExplicitKeysSource
from py2store import add_ipython_key_completions, KvReader, Store, wrap_kvs


# Election dates for supported years
ELECTION_DATES = {
    2016: '2016-11-08',
    2020: '2020-11-03',
    2024: '2024-11-05',
}

# Standard region names (states in lowercase with hyphens)
REGIONS = [
    'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
    'connecticut', 'delaware', 'district-of-columbia', 'florida', 'georgia',
    'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
    'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
    'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new-hampshire',
    'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio',
    'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota',
    'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west-virginia',
    'wisconsin', 'wyoming'
]


def get_election_data(region: str, year: int = 2020) -> Dict[str, Any]:
    """
    Fetch raw election JSON data for a specific region and year from NYT API.

    Args:
        region: Region name (state) in lowercase with hyphens (e.g., 'pennsylvania')
        year: Election year (2016, 2020, or 2024)

    Returns:
        Dictionary containing election data, or requests.Response object on error

    Raises:
        ValueError: If year is not supported

    Example:
        >>> data = get_election_data('florida', 2020)  # doctest: +SKIP
        >>> print(data['data']['races'][0]['state_id'])  # doctest: +SKIP
        'FL'
    """
    if year not in ELECTION_DATES:
        raise ValueError(
            f"Year {year} not supported. Available years: {list(ELECTION_DATES.keys())}"
        )

    election_date = ELECTION_DATES[year]
    url = f'https://static01.nyt.com/elections-assets/{year}/data/api/{election_date}/state-page/{region}.json'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.HTTPError(
            f"Failed to fetch data for region '{region}' and year {year}. "
            f"Status code: {response.status_code}. "
            f"Note: Regions should be in lowercase with hyphens, like: {REGIONS[:5]}..."
        )


@add_ipython_key_completions
@Store.wrap
class ElectionRawJson(ExplicitKeysSource):
    """
    Store interface for accessing raw election JSON data by region.

    Args:
        year: Election year (2016, 2020, or 2024). Defaults to 2020.

    Example:
        >>> store = ElectionRawJson(year=2020)  # doctest: +SKIP
        >>> florida_data = store['florida']  # doctest: +SKIP
        >>> print(florida_data['data']['races'][0]['race_id'])  # doctest: +SKIP
    """

    def __init__(self, year: int = 2020):
        if year not in ELECTION_DATES:
            raise ValueError(
                f"Year {year} not supported. Available years: {list(ELECTION_DATES.keys())}"
            )
        self.year = year
        _obj_of_key = partial(get_election_data, year=year)
        super().__init__(key_collection=REGIONS, _obj_of_key=_obj_of_key)


class Races(ElectionRawJson):
    """
    Store interface for accessing race data by region.

    Transforms raw election data into a store of races indexed by race slug.

    Args:
        year: Election year (2016, 2020, or 2024). Defaults to 2020.

    Example:
        >>> races = Races(year=2020)  # doctest: +SKIP
        >>> pa_races = races['pennsylvania']  # doctest: +SKIP
        >>> president = pa_races['president-general-2020-11-03']  # doctest: +SKIP
    """

    def _obj_of_data(self, data):
        """Transform raw data into a store of races."""
        state_slug = data['data']['races'][0]['state_id'].lower()
        races = Store({x['race_slug'][3:]: x for x in data['data']['races']})
        return add_ipython_key_completions(races)


def _post_process_timeseries(data: Dict[str, Any], race_type: str = 'president') -> pd.DataFrame:
    """
    Post-process race data to extract time series information.

    Args:
        data: Raw election data dictionary
        race_type: Type of race to extract (e.g., 'president', 'senate')

    Returns:
        DataFrame with time series data including vote shares
    """
    # Find the race key matching the race type
    race_key = None
    for key in data.keys():
        if race_type in key.lower() and 'timeseries' in data[key]:
            race_key = key
            break

    if not race_key:
        raise KeyError(f"No race matching type '{race_type}' found with timeseries data")

    df = pd.DataFrame(data[race_key]['timeseries'])
    if 'vote_shares' in df.columns:
        df = pd.concat(
            (df, pd.DataFrame(df['vote_shares'].values.tolist())), axis=1
        )
        del df['vote_shares']

    if 'timestamp' in df.columns:
        df = df.set_index('timestamp')

    return df


def get_races(region: str, year: int = 2020) -> Dict[str, Any]:
    """
    Get races for a specific region and year.

    Args:
        region: Region name (state) in lowercase with hyphens
        year: Election year (2016, 2020, or 2024)

    Returns:
        Dictionary mapping race slugs to race data

    Example:
        >>> races = get_races('pennsylvania', 2020)  # doctest: +SKIP
        >>> list(races.keys())[:2]  # doctest: +SKIP
        ['president-general-2020-11-03', 'senate-general-2020-11-03']
    """
    races_store = Races(year=year)
    return races_store[region]


def get_president_timeseries(region: str, year: int = 2020) -> pd.DataFrame:
    """
    Get president race time series data for a specific region and year.

    Args:
        region: Region name (state) in lowercase with hyphens
        year: Election year (2016, 2020, or 2024)

    Returns:
        DataFrame with time series vote data

    Example:
        >>> df = get_president_timeseries('georgia', 2020)  # doctest: +SKIP
        >>> df.columns  # doctest: +SKIP
        Index(['timestamp', 'votes', 'bidenj', 'trumpd', ...], dtype='object')
    """
    races = get_races(region, year)
    return _post_process_timeseries(races, race_type='president')


# Store classes for backward compatibility with original API
Election2020RawJson = partial(ElectionRawJson, year=2020)
Races2020 = partial(Races, year=2020)
President2020TimeSeries = wrap_kvs(Races2020, obj_of_data=_post_process_timeseries)
