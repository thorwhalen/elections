# elections

Election Data Package

This package provides a unified interface to multiple election data sources from
around the world. It includes U.S. election data from various providers as well as
international parliamentary and election data.

**Available Data Sources:**

- **nytimes**: New York Times election results (2016, 2020, 2024)
- **openfec**: Federal Election Commission campaign finance data
- **google_civic**: Google Civic Information API (polling, representatives, voter info)
- **democracy_works**: Democracy Works election guidance (dates, deadlines, locations)
- **ipu_parline**: Inter-Parliamentary Union global parliamentary data

**Quick Start:**

```pycon
>>> from elections import ElectionsDataModules
>>>
>>> # Access all data sources as a mapping
>>> modules = ElectionsDataModules()
>>> list(modules.keys())
['nytimes', 'openfec', 'google_civic', 'democracy_works', 'ipu_parline']
>>>
>>> # Access a specific data source module
>>> nyt = modules['nytimes']
>>> data = nyt.get_election_data('florida', year=2020)
>>>
>>> # Or import modules directly
>>> from elections import nytimes
>>> data = nytimes.get_election_data('pennsylvania', year=2020)
```

**Consistent Parameter Names:**

Across all modules, we use consistent parameter names for common concepts:

- **year**: Election year (e.g., 2020, 2024)
- **region**: Geographic region (state abbreviation like ‘PA’, or state name like ‘pennsylvania’)
- **api_key**: API authentication key (when required)
- **race_type**: Type of race (e.g., ‘president’, ‘senate’, ‘house’)
- **office**: Office being sought (used by some APIs)

**API Keys:**

Some data sources require API keys:

- **openfec**: Optional (use ‘DEMO_KEY’ or get free key at [https://api.open.fec.gov/developers/](https://api.open.fec.gov/developers/))
- **google_civic**: Required (get free key at [https://console.developers.google.com/](https://console.developers.google.com/))
- **democracy_works**: Not required
- **nytimes**: Not required
- **ipu_parline**: Not required

Set API keys via environment variables:

- OPENFEC_API_KEY
- GOOGLE_CIVIC_API_KEY

**Example Workflows:**

Get NYT election results for multiple states:

```pycon
>>> from elections.nytimes import get_election_data
>>> states = ['florida', 'pennsylvania', 'georgia']
>>> results = {s: get_election_data(s, year=2020) for s in states}
```

Search for campaign finance data:

```pycon
>>> from elections.openfec import search_candidates, get_candidate_totals
>>> candidates = search_candidates('Biden', year=2024)
>>> # Get financial totals for specific candidate
>>> totals = get_candidate_totals('P80001571', year=2020)
```

Get voter information for an address:

```pycon
>>> from elections.google_civic import get_voter_info
>>> info = get_voter_info(
...     '1600 Pennsylvania Ave NW, Washington, DC 20500',
...     api_key='YOUR_KEY'
... )
```

Get international election data:

```pycon
>>> from elections.ipu_parline import get_parliament, get_election_results
>>> france = get_parliament('FRA')
>>> results = get_election_results('DEU')
```

### Functions

| [`get_source`](#elections.get_source)(source_id)   | Convenience function to get a data source module.   |
|--------------------------------------------------------------------------|-----------------------------------------------------|
| [`list_sources`](#elections.list_sources)()          | List all available data source identifiers.         |

### Classes

| [`ElectionsDataModules`](#elections.ElectionsDataModules)()   | Mapping interface to election data sources.   |
|---------------------------------------------------------------------------|-----------------------------------------------|

### *class* elections.ElectionsDataModules

Bases: [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)

Mapping interface to election data sources.

This class provides dict-like access to different election data source modules.
Each key is a source identifier, and the value is the corresponding module.

**Available Sources:**

- ‘nytimes’: New York Times election results API
- ‘openfec’: Federal Election Commission API
- ‘google_civic’: Google Civic Information API
- ‘democracy_works’: Democracy Works Elections API
- ‘ipu_parline’: Inter-Parliamentary Union Parline database

**Usage:**

```pycon
>>> modules = ElectionsDataModules()
>>>
>>> # List all available sources
>>> sources = sorted(modules)
>>> sources
['democracy_works', 'google_civic', 'ipu_parline', 'nytimes', 'openfec']
```

```pycon
>>> # Access a specific source
>>> nyt_module = modules['nytimes']
>>> data = nyt_module.get_election_data('florida', year=2020)
>>>
>>> # Iterate over all sources
>>> for source_id, module in modules.items():
...     print(f"{source_id}: {module.__doc__.split(chr(10))[0]}")
>>>
>>> # Check if a source exists
>>> 'nytimes' in modules
True
```

**Attributes:**

Each source module provides its own functions and classes for accessing data.
See the module documentation for details:

```pycon
>>> modules = ElectionsDataModules()
>>> nyt = modules['nytimes']
>>> help(nyt)
```

#### describe()

Print descriptions of all available data sources.

This method loads each module and prints its first docstring line
along with key information about the data source.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### elections.get_source(source_id)

Convenience function to get a data source module.

* **Parameters:**
  **source_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source identifier (e.g., ‘nytimes’, ‘openfec’)
* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
* **Returns:**
  The data source module

### Example

```pycon
>>> from elections import get_source
>>> nyt = get_source('nytimes')
>>> data = nyt.get_election_data('florida', year=2020)
```

### elections.list_sources()

List all available data source identifiers.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)
* **Returns:**
  List of source identifier strings

### Example

```pycon
>>> from elections import list_sources
>>> sources = list_sources()
>>> 'nytimes' in sources
True
>>> 'openfec' in sources
True
```

### Modules

| [`democracy_works`](elections.democracy_works.html.md#module-elections.democracy_works)   | Democracy Works Elections API Data Source           |
|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`google_civic`](elections.google_civic.html.md#module-elections.google_civic)         | Google Civic Information API Data Source            |
| [`ipu_parline`](elections.ipu_parline.html.md#module-elections.ipu_parline)           | IPU Parline - Inter-Parliamentary Union Data Source |
| [`nytimes`](elections.nytimes.html.md#module-elections.nytimes)                   | New York Times Election Data Source                 |
| [`openfec`](elections.openfec.html.md#module-elections.openfec)                   | OpenFEC - Federal Election Commission Data Source   |
