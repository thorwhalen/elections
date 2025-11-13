"""IPU Parline - Inter-Parliamentary Union Data Source

This module provides access to global parliamentary and election data from the
Inter-Parliamentary Union (IPU) Parline database. The database contains information
on national parliaments worldwide, including election results, turnout, party
composition, and electoral systems for 190+ countries.

**Data Source:** IPU Parline (Inter-Parliamentary Union)
**Base URL:** https://data.ipu.org/api/
**Access:** Free, no API key required
**Coverage:** Global - 190+ countries
**Data Types:** Election results, turnout, party composition, electoral systems, parliamentary info

**More Information:**
- Data Portal: https://data.ipu.org/
- IPU Main Site: https://www.ipu.org/
- About Parline: https://www.ipu.org/resources/parline-database

**Note:** This API provides historical data on national parliaments and elections
worldwide. It's particularly useful for comparative analysis across countries and
for historical election data. Live/real-time election data is not available.

**Country Codes:** Uses ISO 3166-1 alpha-3 codes (e.g., 'USA', 'GBR', 'FRA', 'DEU')

**Example Usage:**

    >>> from elections.ipu_parline import get_parliament, get_election_results, get_country_list  # doctest: +SKIP
    >>>
    >>> # Get parliament information for France
    >>> parliament = get_parliament(country_code='FRA')  # doctest: +SKIP
    >>>
    >>> # Get election results for a country
    >>> results = get_election_results(country_code='DEU')  # doctest: +SKIP
    >>>
    >>> # Get list of available countries
    >>> countries = get_country_list()  # doctest: +SKIP

"""

from typing import Dict, List, Optional, Any
import requests


BASE_URL = 'https://data.ipu.org/api/'

# Common country codes (ISO 3166-1 alpha-3)
COMMON_COUNTRIES = {
    'usa': 'USA', 'united states': 'USA',
    'uk': 'GBR', 'united kingdom': 'GBR', 'britain': 'GBR',
    'france': 'FRA',
    'germany': 'DEU',
    'italy': 'ITA',
    'spain': 'ESP',
    'canada': 'CAN',
    'australia': 'AUS',
    'japan': 'JPN',
    'india': 'IND',
    'brazil': 'BRA',
    'mexico': 'MEX',
    'china': 'CHN',
    'russia': 'RUS',
}


def _normalize_country_code(country_code: str) -> str:
    """
    Normalize country code to ISO 3166-1 alpha-3 format.

    Args:
        country_code: Country code or name

    Returns:
        Normalized 3-letter country code
    """
    code = country_code.strip().upper()

    # If already 3 letters, return as-is
    if len(code) == 3:
        return code

    # Check if it's a common country name
    lookup = COMMON_COUNTRIES.get(country_code.lower())
    if lookup:
        return lookup

    return code


def _make_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make a request to the IPU Parline API.

    Args:
        endpoint: API endpoint path
        params: Optional query parameters

    Returns:
        JSON response as dictionary

    Raises:
        requests.HTTPError: If request fails
    """
    url = BASE_URL + endpoint
    response = requests.get(url, params=params or {})

    if response.status_code == 404:
        raise requests.HTTPError(
            f"Resource not found (404). Check that the country code or endpoint is correct. "
            f"Country codes should be ISO 3166-1 alpha-3 format (e.g., 'FRA', 'GBR', 'USA')."
        )
    elif response.status_code == 400:
        raise requests.HTTPError(
            f"Bad request (400). Check your parameters: {response.text}"
        )
    elif response.status_code != 200:
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def get_parliament(country_code: str) -> Dict[str, Any]:
    """
    Get parliament information for a specific country.

    Args:
        country_code: ISO 3166-1 alpha-3 country code (e.g., 'FRA', 'GBR', 'USA')
                     or common name (e.g., 'France', 'UK')

    Returns:
        Dictionary with parliament information

    Example:
        >>> parliament = get_parliament('FRA')  # doctest: +SKIP
        >>> 'country' in parliament  # doctest: +SKIP
        True
        >>>
        >>> # Can also use country names
        >>> parliament = get_parliament('France')  # doctest: +SKIP
    """
    code = _normalize_country_code(country_code)
    return _make_request(f'parliaments/{code}')


def get_election_results(
    country_code: str,
    chamber: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get election results for a country.

    Args:
        country_code: ISO 3166-1 alpha-3 country code or common name
        chamber: Optional chamber specification ('lower', 'upper', 'unicameral')

    Returns:
        Dictionary with election results

    Example:
        >>> results = get_election_results('DEU')  # doctest: +SKIP
        >>> isinstance(results, dict)  # doctest: +SKIP
        True
    """
    code = _normalize_country_code(country_code)
    endpoint = f'elections/{code}'

    params = {}
    if chamber:
        params['chamber'] = chamber.lower()

    return _make_request(endpoint, params)


def get_country_list() -> List[Dict[str, Any]]:
    """
    Get list of countries available in the database.

    Returns:
        List of dictionaries with country information

    Example:
        >>> countries = get_country_list()  # doctest: +SKIP
        >>> len(countries) > 100  # doctest: +SKIP
        True
        >>> any(c.get('code') == 'USA' for c in countries)  # doctest: +SKIP
        True
    """
    result = _make_request('countries')
    return result if isinstance(result, list) else result.get('countries', [])


def get_women_in_parliament(country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Get statistics on women in national parliaments.

    Args:
        country_code: Optional country code to filter by specific country

    Returns:
        Dictionary with women in parliament statistics

    Example:
        >>> stats = get_women_in_parliament()  # doctest: +SKIP
        >>> isinstance(stats, dict)  # doctest: +SKIP
        True
        >>>
        >>> # For specific country
        >>> stats = get_women_in_parliament('SWE')  # doctest: +SKIP
    """
    if country_code:
        code = _normalize_country_code(country_code)
        return _make_request(f'women-in-parliament/{code}')
    else:
        return _make_request('women-in-parliament')


def get_electoral_system(country_code: str) -> Dict[str, Any]:
    """
    Get electoral system information for a country.

    Args:
        country_code: ISO 3166-1 alpha-3 country code or common name

    Returns:
        Dictionary with electoral system details

    Example:
        >>> system = get_electoral_system('CAN')  # doctest: +SKIP
        >>> isinstance(system, dict)  # doctest: +SKIP
        True
    """
    code = _normalize_country_code(country_code)
    return _make_request(f'electoral-systems/{code}')


def search_parliaments(
    region: Optional[str] = None,
    chamber_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for parliaments by region or chamber type.

    Args:
        region: Optional region to filter (e.g., 'Europe', 'Americas', 'Asia')
        chamber_type: Optional chamber type ('bicameral', 'unicameral')

    Returns:
        List of parliament information

    Example:
        >>> parliaments = search_parliaments(region='Europe')  # doctest: +SKIP
        >>> len(parliaments) > 0  # doctest: +SKIP
        True
    """
    params = {}
    if region:
        params['region'] = region
    if chamber_type:
        params['chamber_type'] = chamber_type.lower()

    result = _make_request('parliaments', params)
    return result if isinstance(result, list) else result.get('parliaments', [])
