"""Democracy Works Elections API Data Source

This module provides access to U.S. election guidance data through the Democracy Works
Elections API, including election dates, deadlines, polling locations, ballot measures,
and candidate information for federal, state, and local levels.

**Data Source:** Democracy Works Elections API
**Base URL:** https://api.democracy.works/elections/v2/
**Access:** Free, no API key required (but may require registration for alerts)
**Coverage:** U.S. federal, state, and local elections
**Data Types:** Election dates, deadlines, polling locations, ballot measures, candidates

**More Information:**
- API Documentation: https://developers.democracy.works/api/v2
- Google Group (for updates): https://groups.google.com/g/turbovote-api
- Main Site: https://www.democracy.works/

**Note:** This API provides voter guidance data including when and where to vote.
It's particularly useful for getting information about upcoming elections, registration
deadlines, and voting locations.

**Example Usage:**

    >>> from elections.democracy_works import get_elections, get_election_by_id, get_state_elections  # doctest: +SKIP
    >>>
    >>> # Get list of all elections
    >>> elections = get_elections()  # doctest: +SKIP
    >>>
    >>> # Get elections for a specific state
    >>> state_elections = get_state_elections(region='PA')  # doctest: +SKIP
    >>>
    >>> # Get detailed info for specific election
    >>> election = get_election_by_id('12345')  # doctest: +SKIP

"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import requests


BASE_URL = 'https://api.democracy.works/elections/v2/'


def _make_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make a request to the Democracy Works Elections API.

    Args:
        endpoint: API endpoint path (e.g., 'elections')
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
            f"Resource not found (404). Check that the election ID or endpoint is correct."
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


def get_elections(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Get list of elections.

    Args:
        date_from: Start date in YYYY-MM-DD format
        date_to: End date in YYYY-MM-DD format
        **kwargs: Additional API parameters

    Returns:
        Dictionary with elections list

    Example:
        >>> elections = get_elections()  # doctest: +SKIP
        >>> len(elections) > 0  # doctest: +SKIP
        True
    """
    params = {}

    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to

    params.update(kwargs)

    return _make_request('elections', params)


def get_election_by_id(election_id: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific election.

    Args:
        election_id: Election ID (obtained from get_elections())

    Returns:
        Dictionary with election details

    Example:
        >>> election = get_election_by_id('12345')  # doctest: +SKIP
        >>> 'id' in election  # doctest: +SKIP
        True
    """
    return _make_request(f'elections/{election_id}')


def get_state_elections(
    region: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Get elections for a specific state.

    Args:
        region: State abbreviation (e.g., 'PA', 'CA')
        date_from: Start date in YYYY-MM-DD format
        date_to: End date in YYYY-MM-DD format
        **kwargs: Additional API parameters

    Returns:
        Dictionary with state elections

    Example:
        >>> elections = get_state_elections('PA')  # doctest: +SKIP
        >>> isinstance(elections, (dict, list))  # doctest: +SKIP
        True
    """
    params = {'state': region.upper()}

    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to

    params.update(kwargs)

    return _make_request('elections', params)


def get_upcoming_elections(
    region: Optional[str] = None,
    days_ahead: int = 90
) -> Dict[str, Any]:
    """
    Get upcoming elections, optionally filtered by state.

    Args:
        region: Optional state abbreviation (e.g., 'PA', 'CA')
        days_ahead: Number of days to look ahead (default 90)

    Returns:
        Dictionary with upcoming elections

    Example:
        >>> elections = get_upcoming_elections(region='CA', days_ahead=60)  # doctest: +SKIP
        >>> isinstance(elections, (dict, list))  # doctest: +SKIP
        True
    """
    from datetime import datetime, timedelta

    today = datetime.now().date()
    future_date = today + timedelta(days=days_ahead)

    params = {
        'date_from': today.isoformat(),
        'date_to': future_date.isoformat()
    }

    if region:
        params['state'] = region.upper()

    return _make_request('elections', params)
