"""Google Civic Information API Data Source

This module provides access to U.S. civic data through Google's Civic Information API,
including elections, representatives, polling places, early voting sites, and candidate
information. The API covers both historical and upcoming elections.

**Data Source:** Google Civic Information API
**Base URL:** https://civicinfo.googleapis.com/civicinfo/v2/
**Access:** Requires free Google API key
**Rate Limits:** 1,000 requests/day (free tier)
**Coverage:** U.S. federal, state, and local elections
**Data Types:** Elections, representatives, polling locations, ballot info, candidates

**Getting an API Key:**
1. Go to: https://console.developers.google.com/
2. Create a new project (or select existing)
3. Enable the "Google Civic Information API"
4. Go to "Credentials" and create an API key
5. Set via environment variable: export GOOGLE_CIVIC_API_KEY='your_key'

**More Information:**
- API Documentation: https://developers.google.com/civic-information/docs/v2
- API Console: https://console.developers.google.com/apis/library/civicinfo.googleapis.com
- Data Coverage: https://developers.google.com/civic-information/docs/v2/coverage

**Error Messages:**
If you receive an authentication error, you need a Google API key:
1. Register at: https://console.developers.google.com/
2. Enable the Civic Information API for your project
3. Create an API key in the Credentials section

**Example Usage:**

    >>> from elections.google_civic import get_elections, get_voter_info, get_representatives  # doctest: +SKIP
    >>>
    >>> # Get list of available elections
    >>> elections = get_elections(api_key='YOUR_KEY')  # doctest: +SKIP
    >>>
    >>> # Get voter information for an address
    >>> voter_info = get_voter_info(  # doctest: +SKIP
    ...     address='1600 Pennsylvania Ave NW, Washington, DC',
    ...     api_key='YOUR_KEY'
    ... )
    >>>
    >>> # Get representatives for an address
    >>> reps = get_representatives(  # doctest: +SKIP
    ...     address='340 Main St, Venice, CA 90291',
    ...     api_key='YOUR_KEY'
    ... )

"""

import os
from typing import Dict, List, Optional, Any
import requests


BASE_URL = 'https://civicinfo.googleapis.com/civicinfo/v2/'


def _get_api_key(api_key: Optional[str] = None) -> str:
    """
    Get API key from parameter or environment.

    Args:
        api_key: Optional API key to use

    Returns:
        API key string

    Raises:
        ValueError: If no API key is available
    """
    if api_key:
        return api_key

    env_key = os.environ.get('GOOGLE_CIVIC_API_KEY')
    if env_key:
        return env_key

    raise ValueError(
        "Google Civic Information API requires an API key. "
        "Get a free key at: https://console.developers.google.com/apis/library/civicinfo.googleapis.com "
        "Then either:\n"
        "  1. Pass it as api_key parameter\n"
        "  2. Set environment variable: export GOOGLE_CIVIC_API_KEY='your_key'"
    )


def _make_request(
    endpoint: str,
    params: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a request to the Google Civic Information API.

    Args:
        endpoint: API endpoint path (e.g., 'elections')
        params: Query parameters
        api_key: Optional API key

    Returns:
        JSON response as dictionary

    Raises:
        requests.HTTPError: If request fails
        ValueError: If API key is missing
    """
    params['key'] = _get_api_key(api_key)
    url = BASE_URL + endpoint

    response = requests.get(url, params=params)

    if response.status_code == 400:
        error_msg = response.json().get('error', {}).get('message', response.text)
        raise requests.HTTPError(
            f"Bad request (400): {error_msg}. "
            f"Check your parameters and ensure addresses are properly formatted."
        )
    elif response.status_code == 401 or response.status_code == 403:
        raise requests.HTTPError(
            f"Authentication failed ({response.status_code}). "
            f"Your API key may be invalid or the API is not enabled for your project. "
            f"Get a free API key at: https://console.developers.google.com/apis/library/civicinfo.googleapis.com"
        )
    elif response.status_code == 429:
        raise requests.HTTPError(
            f"Rate limit exceeded (429). Free tier allows 1,000 requests/day. "
            f"Check your quota at: https://console.developers.google.com/"
        )
    elif response.status_code != 200:
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def get_elections(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get list of available elections.

    Returns information about current and upcoming elections, including election IDs
    that can be used with get_voter_info().

    Args:
        api_key: Google Civic Information API key

    Returns:
        Dictionary with 'elections' list containing election details

    Example:
        >>> elections = get_elections(api_key='YOUR_KEY')  # doctest: +SKIP
        >>> len(elections['elections']) > 0  # doctest: +SKIP
        True
        >>> elections['elections'][0]['name']  # doctest: +SKIP
        'U.S. General Election'
    """
    return _make_request('elections', {}, api_key)


def get_voter_info(
    address: str,
    election_id: Optional[int] = None,
    api_key: Optional[str] = None,
    return_all_available_data: bool = True
) -> Dict[str, Any]:
    """
    Get voter information for a specific address.

    Returns polling locations, early vote sites, ballot information, and candidates
    for the given address.

    Args:
        address: Full address (street, city, state, ZIP)
        election_id: Optional election ID (get from get_elections())
        api_key: Google Civic Information API key
        return_all_available_data: If True, returns all available data

    Returns:
        Dictionary with election info, polling locations, candidates, etc.

    Example:
        >>> info = get_voter_info(  # doctest: +SKIP
        ...     '1600 Pennsylvania Ave NW, Washington, DC 20500',
        ...     api_key='YOUR_KEY'
        ... )
        >>> 'pollingLocations' in info or 'contests' in info  # doctest: +SKIP
        True
    """
    params = {
        'address': address,
        'returnAllAvailableData': str(return_all_available_data).lower()
    }

    if election_id:
        params['electionId'] = election_id

    return _make_request('voterinfo', params, api_key)


def get_representatives(
    address: Optional[str] = None,
    include_offices: bool = True,
    levels: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get elected representatives for an address.

    Returns information about federal, state, and local elected officials.

    Args:
        address: Full address (if not provided, uses national divisions)
        include_offices: Whether to include office information
        levels: List of government levels ('country', 'administrativeArea1', 'locality')
        roles: List of roles ('legislatorUpperBody', 'legislatorLowerBody', 'headOfGovernment')
        api_key: Google Civic Information API key

    Returns:
        Dictionary with divisions, offices, and officials

    Example:
        >>> reps = get_representatives(  # doctest: +SKIP
        ...     '340 Main St, Venice, CA 90291',
        ...     api_key='YOUR_KEY'
        ... )
        >>> 'officials' in reps  # doctest: +SKIP
        True
    """
    params = {'includeOffices': str(include_offices).lower()}

    if address:
        params['address'] = address
    if levels:
        params['levels'] = levels
    if roles:
        params['roles'] = roles

    return _make_request('representatives', params, api_key)


def get_representatives_by_division(
    division_id: str,
    levels: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get representatives for a specific Open Civic Data division.

    Args:
        division_id: OCD division ID (e.g., 'ocd-division/country:us/state:ca')
        levels: List of government levels to filter
        roles: List of roles to filter
        api_key: Google Civic Information API key

    Returns:
        Dictionary with offices and officials for the division

    Example:
        >>> reps = get_representatives_by_division(  # doctest: +SKIP
        ...     'ocd-division/country:us/state:ca',
        ...     api_key='YOUR_KEY'
        ... )
        >>> 'officials' in reps  # doctest: +SKIP
        True
    """
    params = {}

    if levels:
        params['levels'] = levels
    if roles:
        params['roles'] = roles

    endpoint = f'representatives/{division_id}'
    return _make_request(endpoint, params, api_key)
