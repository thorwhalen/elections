# elections.nytimes

New York Times Election Data Source

This module provides access to election data from the New York Times’ unofficial
election results API. The API provides detailed election results including vote
counts, candidate information, and time-series data for U.S. elections.

**Data Source:** New York Times Elections Assets API (unofficial)
**URL Pattern:** [https://static01.nyt.com/elections-assets](https://static01.nyt.com/elections-assets)/{year}/data/api/{date}/…
**Access:** Free, no API key required
**Coverage:** U.S. presidential and other races for 2016, 2020, 2024
**Data Types:** Election results, vote counts, time-series data, race details

**More Information:**

- Example usage: [https://gist.github.com/curran/b218499a412033064fea7936334b86bb](https://gist.github.com/curran/b218499a412033064fea7936334b86bb)
- Background: [https://source.opennews.org/articles/ny-times-results-loader/](https://source.opennews.org/articles/ny-times-results-loader/)

**Note:** This is an unofficial API that powers the NYT election website. The API
structure has been consistent across election years but is not officially documented
or guaranteed to remain available.

**Example Usage:**

#### NOTE
I only managed to get data for year=2020. I implemented the patterns for other years,
but it doesn’t seem to work.

```pycon
>>> from elections.nytimes import get_election_data, get_races, get_president_timeseries
>>>
>>> # Get raw election data for Pennsylvania in 2020
>>> data = get_election_data(region='pennsylvania')
>>>
>>> # Get races for a specific state
>>> races = get_races(region='florida')
>>>
>>> # Get president race time series
>>> timeseries = get_president_timeseries(region='georgia')
```

### Functions

| [`get_election_data`](#elections.nytimes.get_election_data)(region[, year])        | Fetch raw election JSON data for a specific region and year from NYT API.   |
|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [`get_president_timeseries`](#elections.nytimes.get_president_timeseries)(region[, year]) | Get president race time series data for a specific region and year.         |
| [`get_races`](#elections.nytimes.get_races)(region[, year])                | Get races for a specific region and year.                                   |

### Classes

| [`Races`](#elections.nytimes.Races)([year])   | Store interface for accessing race data by region.   |
|------------------------------------------------------------------|------------------------------------------------------|

### *class* elections.nytimes.Races(year=2020)

Bases: `Store`

Store interface for accessing race data by region.

Transforms raw election data into a store of races indexed by race slug.

* **Parameters:**
  **year** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Election year (2016, 2020, or 2024). Defaults to 2020.

### Example

```pycon
>>> races = Races(year=2020)
>>> pa_races = races['pennsylvania']
>>> president = pa_races['president-general-2020-11-03']
```

### elections.nytimes.get_election_data(region, year=2020)

Fetch raw election JSON data for a specific region and year from NYT API.

* **Parameters:**
  * **region** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Region name (state) in lowercase with hyphens (e.g., ‘pennsylvania’)
  * **year** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Election year (2016, 2020, or 2024)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary containing election data, or requests.Response object on error
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If year is not supported

### Example

```pycon
>>> data = get_election_data('florida', 2020)
>>> print(data['data']['races'][0]['state_id'])
'FL'
```

### elections.nytimes.get_president_timeseries(region, year=2020)

Get president race time series data for a specific region and year.

* **Parameters:**
  * **region** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Region name (state) in lowercase with hyphens
  * **year** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Election year (2016, 2020, or 2024)
* **Return type:**
  `DataFrame`
* **Returns:**
  DataFrame with time series vote data

### Example

```pycon
>>> df = get_president_timeseries('georgia', 2020)
>>> df.columns
Index(['timestamp', 'votes', 'bidenj', 'trumpd', ...], dtype='object')
```

### elections.nytimes.get_races(region, year=2020)

Get races for a specific region and year.

* **Parameters:**
  * **region** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Region name (state) in lowercase with hyphens
  * **year** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Election year (2016, 2020, or 2024)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary mapping race slugs to race data

### Example

```pycon
>>> races = get_races('pennsylvania', 2020)
>>> list(races.keys())[:2]
['president-general-2020-11-03', 'senate-general-2020-11-03']
```
