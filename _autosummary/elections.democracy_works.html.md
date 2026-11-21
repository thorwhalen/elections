# elections.democracy_works

Democracy Works Elections API Data Source

This module provides access to U.S. election guidance data through the Democracy Works
Elections API, including election dates, deadlines, polling locations, ballot measures,
and candidate information for federal, state, and local levels.

**Data Source:** Democracy Works Elections API
**Base URL:** [https://api.democracy.works/elections/v2/](https://api.democracy.works/elections/v2/)
**Access:** Free, no API key required (but may require registration for alerts)
**Coverage:** U.S. federal, state, and local elections
**Data Types:** Election dates, deadlines, polling locations, ballot measures, candidates

**More Information:**

- API Documentation: [https://developers.democracy.works/api/v2](https://developers.democracy.works/api/v2)
- Google Group (for updates): [https://groups.google.com/g/turbovote-api](https://groups.google.com/g/turbovote-api)
- Main Site: [https://www.democracy.works/](https://www.democracy.works/)

**Note:** This API provides voter guidance data including when and where to vote.
It’s particularly useful for getting information about upcoming elections, registration
deadlines, and voting locations.

**Example Usage:**

```pycon
>>> from elections.democracy_works import get_elections, get_election_by_id, get_state_elections
>>>
>>> # Get list of all elections
>>> elections = get_elections()
>>>
>>> # Get elections for a specific state
>>> state_elections = get_state_elections(region='PA')
>>>
>>> # Get detailed info for specific election
>>> election = get_election_by_id('12345')
```

### Functions

| [`get_election_by_id`](#elections.democracy_works.get_election_by_id)(election_id)                   | Get detailed information for a specific election.     |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| [`get_elections`](#elections.democracy_works.get_elections)([date_from, date_to])               | Get list of elections.                                |
| [`get_state_elections`](#elections.democracy_works.get_state_elections)(region[, date_from, date_to]) | Get elections for a specific state.                   |
| [`get_upcoming_elections`](#elections.democracy_works.get_upcoming_elections)([region, days_ahead])      | Get upcoming elections, optionally filtered by state. |

### elections.democracy_works.get_election_by_id(election_id)

Get detailed information for a specific election.

* **Parameters:**
  **election_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Election ID (obtained from get_elections())
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with election details

### Example

```pycon
>>> election = get_election_by_id('12345')
>>> 'id' in election
True
```

### elections.democracy_works.get_elections(date_from=None, date_to=None, \*\*kwargs)

Get list of elections.

* **Parameters:**
  * **date_from** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Start date in YYYY-MM-DD format
  * **date_to** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – End date in YYYY-MM-DD format
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with elections list

### Example

```pycon
>>> elections = get_elections()
>>> len(elections) > 0
True
```

### elections.democracy_works.get_state_elections(region, date_from=None, date_to=None, \*\*kwargs)

Get elections for a specific state.

* **Parameters:**
  * **region** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State abbreviation (e.g., ‘PA’, ‘CA’)
  * **date_from** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Start date in YYYY-MM-DD format
  * **date_to** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – End date in YYYY-MM-DD format
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with state elections

### Example

```pycon
>>> elections = get_state_elections('PA')
>>> isinstance(elections, (dict, list))
True
```

### elections.democracy_works.get_upcoming_elections(region=None, days_ahead=90)

Get upcoming elections, optionally filtered by state.

* **Parameters:**
  * **region** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional state abbreviation (e.g., ‘PA’, ‘CA’)
  * **days_ahead** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Number of days to look ahead (default 90)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with upcoming elections

### Example

```pycon
>>> elections = get_upcoming_elections(region='CA', days_ahead=60)
>>> isinstance(elections, (dict, list))
True
```
