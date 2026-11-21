# elections.openfec

OpenFEC - Federal Election Commission Data Source

This module provides access to federal campaign finance data from the Federal
Election Commission (FEC) through their OpenFEC API. The API offers comprehensive
data on candidates, committees, contributions, expenditures, and filings.

**Data Source:** OpenFEC API (Federal Election Commission)
**Base URL:** [https://api.open.fec.gov/v1/](https://api.open.fec.gov/v1/)
**Access:** Free with optional API key for higher rate limits
**Rate Limits:**

> - Without key: 1,000 calls/hour
> - With key: Up to 120 calls/minute

**Coverage:** Federal elections (Presidential, Senate, House)
**Data Types:** Campaign finance, candidates, committees, contributions, expenditures

**Getting an API Key:**
Register for a free API key at: [https://api.open.fec.gov/developers/](https://api.open.fec.gov/developers/)
Simply provide your email address - no payment required.

**More Information:**

- API Documentation: [https://api.open.fec.gov/developers/](https://api.open.fec.gov/developers/)
- OpenAPI/Swagger UI: [https://api.open.fec.gov/developers/](https://api.open.fec.gov/developers/)
- Data Catalog: [https://www.fec.gov/data/](https://www.fec.gov/data/)

**Error Messages:**
If you receive a 403 or rate limit error without an API key, you can:

1. Use ‘DEMO_KEY’ for testing (limited)
2. Register for a free API key at [https://api.open.fec.gov/developers/](https://api.open.fec.gov/developers/)
3. Set your key via environment variable: export OPENFEC_API_KEY=’your_key’

**Example Usage:**

```pycon
>>> from elections.openfec import get_candidates, get_committees, search_candidates
>>>
>>> # Get candidates for 2024 presidential election
>>> candidates = get_candidates(year=2024, office='president')
>>>
>>> # Search for specific candidate
>>> results = search_candidates('Biden', year=2024)
>>>
>>> # Get committee information
>>> committees = get_committees(year=2024)
```

### Functions

| [`get_candidate_totals`](#elections.openfec.get_candidate_totals)(candidate_id[, year, ...])   | Get financial totals for a specific candidate.   |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------|
| [`get_candidates`](#elections.openfec.get_candidates)([year, office, region, ...])       | Fetch federal election candidates.               |
| [`get_committees`](#elections.openfec.get_committees)([year, committee_type, ...])       | Fetch federal election committees.               |
| [`get_election_results`](#elections.openfec.get_election_results)(year, office[, region, ...]) | Get election results summary.                    |
| [`search_candidates`](#elections.openfec.search_candidates)(name[, year, api_key])          | Search for candidates by name.                   |

### elections.openfec.get_candidate_totals(candidate_id, year=None, api_key=None, \*\*kwargs)

Get financial totals for a specific candidate.

* **Parameters:**
  * **candidate_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – FEC candidate ID (e.g., ‘P80001571’ for Obama)
  * **year** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Election cycle year
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – OpenFEC API key
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with financial totals (receipts, disbursements, etc.)

### Example

```pycon
>>> totals = get_candidate_totals('P80001571', year=2012)
>>> 'results' in totals
True
```

### elections.openfec.get_candidates(year=None, office=None, region=None, party=None, api_key=None, \*\*kwargs)

Fetch federal election candidates.

* **Parameters:**
  * **year** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Election year (e.g., 2024, 2020)
  * **office** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Office type - ‘president’, ‘senate’, ‘house’ (or ‘P’, ‘S’, ‘H’)
  * **region** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – State abbreviation (e.g., ‘PA’, ‘CA’) - for Senate/House
  * **party** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Party abbreviation (e.g., ‘DEM’, ‘REP’, ‘LIB’)
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – OpenFEC API key (defaults to DEMO_KEY or env variable)
  * **\*\*kwargs** – Additional API parameters (per_page, page, sort, etc.)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with ‘results’ list and pagination info

### Example

```pycon
>>> # Get 2024 presidential candidates
>>> data = get_candidates(year=2024, office='president')
>>> len(data['results']) > 0
True
>>>
>>> # Get Pennsylvania senate candidates
>>> data = get_candidates(year=2024, office='senate', region='PA')
```

### elections.openfec.get_committees(year=None, committee_type=None, region=None, api_key=None, \*\*kwargs)

Fetch federal election committees.

* **Parameters:**
  * **year** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Election year
  * **committee_type** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Type of committee (e.g., ‘P’ for Presidential)
  * **region** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – State abbreviation
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – OpenFEC API key
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with committee information

### Example

```pycon
>>> committees = get_committees(year=2024, committee_type='P')
>>> len(committees['results']) > 0
True
```

### elections.openfec.get_election_results(year, office, region=None, api_key=None, \*\*kwargs)

Get election results summary.

* **Parameters:**
  * **year** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Election year
  * **office** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Office type - ‘president’, ‘senate’, or ‘house’
  * **region** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – State abbreviation (for Senate/House)
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – OpenFEC API key
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with election results

### Example

```pycon
>>> results = get_election_results(2020, 'president')
>>> len(results['results']) > 0
True
```

### elections.openfec.search_candidates(name, year=None, api_key=None, \*\*kwargs)

Search for candidates by name.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Candidate name or partial name to search
  * **year** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Optional election year to filter
  * **api_key** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – OpenFEC API key
  * **\*\*kwargs** – Additional API parameters
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with matching candidates

### Example

```pycon
>>> results = search_candidates('Biden', year=2024)
>>> len(results['results']) > 0
True
```
