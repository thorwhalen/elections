"""OpenFEC - Federal Election Commission Data Source

This module provides access to federal campaign finance data from the Federal
Election Commission (FEC) through their OpenFEC API. The API offers comprehensive
data on candidates, committees, contributions, expenditures, and filings.

**Data Source:** OpenFEC API (Federal Election Commission)
**Base URL:** https://api.open.fec.gov/v1/
**Access:** Free with optional API key for higher rate limits
**Rate Limits:**
  - Without key: 1,000 calls/hour
  - With key: Up to 120 calls/minute
**Coverage:** Federal elections (Presidential, Senate, House)
**Data Types:** Campaign finance, candidates, committees, contributions, expenditures

**Getting an API Key:**
Register for a free API key at: https://api.open.fec.gov/developers/
Simply provide your email address - no payment required.

**More Information:**
- API Documentation: https://api.open.fec.gov/developers/
- OpenAPI/Swagger UI: https://api.open.fec.gov/developers/
- Data Catalog: https://www.fec.gov/data/

**Error Messages:**
If you receive a 403 or rate limit error without an API key, you can:
1. Use 'DEMO_KEY' for testing (limited)
2. Register for a free API key at https://api.open.fec.gov/developers/
3. Set your key via environment variable: export OPENFEC_API_KEY='your_key'

**Example Usage:**

    >>> from elections.openfec import get_candidates, get_committees, search_candidates  # doctest: +SKIP
    >>>
    >>> # Get candidates for 2024 presidential election
    >>> candidates = get_candidates(year=2024, office='president')  # doctest: +SKIP
    >>>
    >>> # Search for specific candidate
    >>> results = search_candidates('Biden', year=2024)  # doctest: +SKIP
    >>>
    >>> # Get committee information
    >>> committees = get_committees(year=2024)  # doctest: +SKIP

"""

import os
from typing import Dict, List, Optional, Any
import requests


# Default API key (can be overridden)
DEFAULT_API_KEY = 'DEMO_KEY'
BASE_URL = 'https://api.open.fec.gov/v1/'

# Valid office types
OFFICE_TYPES = ['president', 'senate', 'house', 'P', 'S', 'H']


def _get_api_key(api_key: Optional[str] = None) -> str:
    """
    Get API key from parameter, environment, or default.

    Args:
        api_key: Optional API key to use

    Returns:
        API key string
    """
    if api_key:
        return api_key
    return os.environ.get('OPENFEC_API_KEY', DEFAULT_API_KEY)


def _make_request(
    endpoint: str,
    params: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a request to the OpenFEC API.

    Args:
        endpoint: API endpoint path (e.g., 'candidates/')
        params: Query parameters
        api_key: Optional API key

    Returns:
        JSON response as dictionary

    Raises:
        requests.HTTPError: If request fails
    """
    params['api_key'] = _get_api_key(api_key)
    url = BASE_URL + endpoint

    response = requests.get(url, params=params)

    if response.status_code == 403:
        raise requests.HTTPError(
            f"Access forbidden (403). Your API key may be invalid or you've hit rate limits. "
            f"Get a free API key at: https://api.open.fec.gov/developers/ "
            f"Current key being used: {params['api_key'][:10]}..."
        )
    elif response.status_code == 429:
        raise requests.HTTPError(
            f"Rate limit exceeded (429). "
            f"Without an API key: 1,000 calls/hour. With key: 120 calls/minute. "
            f"Get a free API key at: https://api.open.fec.gov/developers/"
        )
    elif response.status_code != 200:
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def get_candidates(
    year: Optional[int] = None,
    office: Optional[str] = None,
    region: Optional[str] = None,
    party: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Fetch federal election candidates.

    Args:
        year: Election year (e.g., 2024, 2020)
        office: Office type - 'president', 'senate', 'house' (or 'P', 'S', 'H')
        region: State abbreviation (e.g., 'PA', 'CA') - for Senate/House
        party: Party abbreviation (e.g., 'DEM', 'REP', 'LIB')
        api_key: OpenFEC API key (defaults to DEMO_KEY or env variable)
        **kwargs: Additional API parameters (per_page, page, sort, etc.)

    Returns:
        Dictionary with 'results' list and pagination info

    Example:
        >>> # Get 2024 presidential candidates
        >>> data = get_candidates(year=2024, office='president')  # doctest: +SKIP
        >>> len(data['results']) > 0  # doctest: +SKIP
        True
        >>>
        >>> # Get Pennsylvania senate candidates
        >>> data = get_candidates(year=2024, office='senate', region='PA')  # doctest: +SKIP
    """
    params = {}

    if year:
        params['election_year'] = year
    if office:
        # Normalize office to single letter
        office_map = {'president': 'P', 'senate': 'S', 'house': 'H'}
        params['office'] = office_map.get(office.lower(), office.upper())
    if region:
        params['state'] = region.upper()
    if party:
        params['party'] = party.upper()

    params.update(kwargs)

    return _make_request('candidates/', params, api_key)


def search_candidates(
    name: str,
    year: Optional[int] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Search for candidates by name.

    Args:
        name: Candidate name or partial name to search
        year: Optional election year to filter
        api_key: OpenFEC API key
        **kwargs: Additional API parameters

    Returns:
        Dictionary with matching candidates

    Example:
        >>> results = search_candidates('Biden', year=2024)  # doctest: +SKIP
        >>> len(results['results']) > 0  # doctest: +SKIP
        True
    """
    params = {'q': name}
    if year:
        params['election_year'] = year

    params.update(kwargs)

    return _make_request('candidates/search/', params, api_key)


def get_committees(
    year: Optional[int] = None,
    committee_type: Optional[str] = None,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Fetch federal election committees.

    Args:
        year: Election year
        committee_type: Type of committee (e.g., 'P' for Presidential)
        region: State abbreviation
        api_key: OpenFEC API key
        **kwargs: Additional API parameters

    Returns:
        Dictionary with committee information

    Example:
        >>> committees = get_committees(year=2024, committee_type='P')  # doctest: +SKIP
        >>> len(committees['results']) > 0  # doctest: +SKIP
        True
    """
    params = {}

    if year:
        params['cycle'] = year
    if committee_type:
        params['committee_type'] = committee_type.upper()
    if region:
        params['state'] = region.upper()

    params.update(kwargs)

    return _make_request('committees/', params, api_key)


def get_candidate_totals(
    candidate_id: str,
    year: Optional[int] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Get financial totals for a specific candidate.

    Args:
        candidate_id: FEC candidate ID (e.g., 'P80001571' for Obama)
        year: Election cycle year
        api_key: OpenFEC API key
        **kwargs: Additional API parameters

    Returns:
        Dictionary with financial totals (receipts, disbursements, etc.)

    Example:
        >>> totals = get_candidate_totals('P80001571', year=2012)  # doctest: +SKIP
        >>> 'results' in totals  # doctest: +SKIP
        True
    """
    params = {}
    if year:
        params['cycle'] = year

    params.update(kwargs)

    endpoint = f'candidate/{candidate_id}/totals/'
    return _make_request(endpoint, params, api_key)


def get_election_results(
    year: int,
    office: str,
    region: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Get election results summary.

    Args:
        year: Election year
        office: Office type - 'president', 'senate', or 'house'
        region: State abbreviation (for Senate/House)
        api_key: OpenFEC API key
        **kwargs: Additional API parameters

    Returns:
        Dictionary with election results

    Example:
        >>> results = get_election_results(2020, 'president')  # doctest: +SKIP
        >>> len(results['results']) > 0  # doctest: +SKIP
        True
    """
    params = {'election_year': year}

    office_map = {'president': 'president', 'senate': 'senate', 'house': 'house'}
    params['office'] = office_map.get(office.lower(), office.lower())

    if region:
        params['state'] = region.upper()

    params.update(kwargs)

    return _make_request('election/', params, api_key)
