# elections.google_civic

Google Civic Information API Data Source

This module provides access to U.S. civic data through Google’s Civic Information API,
including elections, representatives, polling places, early voting sites, and candidate
information. The API covers both historical and upcoming elections.

**Data Source:** Google Civic Information API
**Base URL:** [https://civicinfo.googleapis.com/civicinfo/v2/](https://civicinfo.googleapis.com/civicinfo/v2/)
**Access:** Requires free Google API key
**Rate Limits:** 1,000 requests/day (free tier)
**Coverage:** U.S. federal, state, and local elections
**Data Types:** Elections, representatives, polling locations, ballot info, candidates

**Getting an API Key:**

1. Go to: [https://console.developers.google.com/](https://console.developers.google.com/)
2. Create a new project (or select existing)
3. Enable the “Google Civic Information API”
4. Go to “Credentials” and create an API key
5. Set via environment variable: export GOOGLE_CIVIC_API_KEY=’your_key’

**More Information:**

- API Documentation: [https://developers.google.com/civic-information/docs/v2](https://developers.google.com/civic-information/docs/v2)
- API Console: [https://console.developers.google.com/apis/library/civicinfo.googleapis.com](https://console.developers.google.com/apis/library/civicinfo.googleapis.com)
- Data Coverage: [https://developers.google.com/civic-information/docs/v2/coverage](https://developers.google.com/civic-information/docs/v2/coverage)

**Error Messages:**
If you receive an authentication error, you need a Google API key:

1. Register at: [https://console.developers.google.com/](https://console.developers.google.com/)
2. Enable the Civic Information API for your project
3. Create an API key in the Credentials section

**Example Usage:**

```pycon
>>> from elections.google_civic import get_elections, get_voter_info, get_representatives
>>>
>>> # Get list of available elections
>>> elections = get_elections(api_key='YOUR_KEY')
>>>
>>> # Get voter information for an address
>>> voter_info = get_voter_info(
...     address='1600 Pennsylvania Ave NW, Washington, DC',
...     api_key='YOUR_KEY'
... )
>>>
>>> # Get representatives for an address
>>> reps = get_representatives(
...     address='340 Main St, Venice, CA 90291',
...     api_key='YOUR_KEY'
... )
```

### Functions

| [`get_elections`](#elections.google_civic.get_elections)([api_key])                     | Get list of available elections.                             |
|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`get_representatives`](#elections.google_civic.get_representatives)([address, ...])          | Get elected representatives for an address.                  |
| [`get_representatives_by_division`](#elections.google_civic.get_representatives_by_division)(division_id) | Get representatives for a specific Open Civic Data division. |
| [`get_voter_info`](#elections.google_civic.get_voter_info)(address[, election_id, ...])  | Get voter information for a specific address.                |

### elections.google_civic.get_elections(api_key=None)

Get list of available elections.

Returns information about current and upcoming elections, including election IDs
that can be used with get_voter_info().

* **Parameters:**
  **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Google Civic Information API key
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with ‘elections’ list containing election details

### Example

```pycon
>>> elections = get_elections(api_key='YOUR_KEY')
>>> len(elections['elections']) > 0
True
>>> elections['elections'][0]['name']
'U.S. General Election'
```

### elections.google_civic.get_representatives(address=None, include_offices=True, levels=None, roles=None, api_key=None)

Get elected representatives for an address.

Returns information about federal, state, and local elected officials.

* **Parameters:**
  * **address** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Full address (if not provided, uses national divisions)
  * **include_offices** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to include office information
  * **levels** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of government levels (‘country’, ‘administrativeArea1’, ‘locality’)
  * **roles** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of roles (‘legislatorUpperBody’, ‘legislatorLowerBody’, ‘headOfGovernment’)
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Google Civic Information API key
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with divisions, offices, and officials

### Example

```pycon
>>> reps = get_representatives(
...     '340 Main St, Venice, CA 90291',
...     api_key='YOUR_KEY'
... )
>>> 'officials' in reps
True
```

### elections.google_civic.get_representatives_by_division(division_id, levels=None, roles=None, api_key=None)

Get representatives for a specific Open Civic Data division.

* **Parameters:**
  * **division_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – OCD division ID (e.g., ‘ocd-division/country:us/state:ca’)
  * **levels** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of government levels to filter
  * **roles** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of roles to filter
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Google Civic Information API key
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with offices and officials for the division

### Example

```pycon
>>> reps = get_representatives_by_division(
...     'ocd-division/country:us/state:ca',
...     api_key='YOUR_KEY'
... )
>>> 'officials' in reps
True
```

### elections.google_civic.get_voter_info(address, election_id=None, api_key=None, return_all_available_data=True)

Get voter information for a specific address.

Returns polling locations, early vote sites, ballot information, and candidates
for the given address.

* **Parameters:**
  * **address** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Full address (street, city, state, ZIP)
  * **election_id** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Optional election ID (get from get_elections())
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Google Civic Information API key
  * **return_all_available_data** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, returns all available data
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with election info, polling locations, candidates, etc.

### Example

```pycon
>>> info = get_voter_info(
...     '1600 Pennsylvania Ave NW, Washington, DC 20500',
...     api_key='YOUR_KEY'
... )
>>> 'pollingLocations' in info or 'contests' in info
True
```
