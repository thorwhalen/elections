# elections.ipu_parline

IPU Parline - Inter-Parliamentary Union Data Source

This module provides access to global parliamentary and election data from the
Inter-Parliamentary Union (IPU) Parline database. The database contains information
on national parliaments worldwide, including election results, turnout, party
composition, and electoral systems for 190+ countries.

**Data Source:** IPU Parline (Inter-Parliamentary Union)
**Base URL:** [https://data.ipu.org/api/](https://data.ipu.org/api/)
**Access:** Free, no API key required
**Coverage:** Global - 190+ countries
**Data Types:** Election results, turnout, party composition, electoral systems, parliamentary info

**More Information:**

- Data Portal: [https://data.ipu.org/](https://data.ipu.org/)
- IPU Main Site: [https://www.ipu.org/](https://www.ipu.org/)
- About Parline: [https://www.ipu.org/resources/parline-database](https://www.ipu.org/resources/parline-database)

**Note:** This API provides historical data on national parliaments and elections
worldwide. It’s particularly useful for comparative analysis across countries and
for historical election data. Live/real-time election data is not available.

**Country Codes:** Uses ISO 3166-1 alpha-3 codes (e.g., ‘USA’, ‘GBR’, ‘FRA’, ‘DEU’)

**Example Usage:**

```pycon
>>> from elections.ipu_parline import get_parliament, get_election_results, get_country_list
>>>
>>> # Get parliament information for France
>>> parliament = get_parliament(country_code='FRA')
>>>
>>> # Get election results for a country
>>> results = get_election_results(country_code='DEU')
>>>
>>> # Get list of available countries
>>> countries = get_country_list()
```

### Functions

| [`get_country_list`](#elections.ipu_parline.get_country_list)()                            | Get list of countries available in the database.   |
|------------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`get_election_results`](#elections.ipu_parline.get_election_results)(country_code[, chamber]) | Get election results for a country.                |
| [`get_electoral_system`](#elections.ipu_parline.get_electoral_system)(country_code)            | Get electoral system information for a country.    |
| [`get_parliament`](#elections.ipu_parline.get_parliament)(country_code)                  | Get parliament information for a specific country. |
| [`get_women_in_parliament`](#elections.ipu_parline.get_women_in_parliament)([country_code])       | Get statistics on women in national parliaments.   |
| [`search_parliaments`](#elections.ipu_parline.search_parliaments)([region, chamber_type])    | Search for parliaments by region or chamber type.  |

### elections.ipu_parline.get_country_list()

Get list of countries available in the database.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Returns:**
  List of dictionaries with country information

### Example

```pycon
>>> countries = get_country_list()
>>> len(countries) > 100
True
>>> any(c.get('code') == 'USA' for c in countries)
True
```

### elections.ipu_parline.get_election_results(country_code, chamber=None)

Get election results for a country.

* **Parameters:**
  * **country_code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ISO 3166-1 alpha-3 country code or common name
  * **chamber** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional chamber specification (‘lower’, ‘upper’, ‘unicameral’)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with election results

### Example

```pycon
>>> results = get_election_results('DEU')
>>> isinstance(results, dict)
True
```

### elections.ipu_parline.get_electoral_system(country_code)

Get electoral system information for a country.

* **Parameters:**
  **country_code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ISO 3166-1 alpha-3 country code or common name
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with electoral system details

### Example

```pycon
>>> system = get_electoral_system('CAN')
>>> isinstance(system, dict)
True
```

### elections.ipu_parline.get_parliament(country_code)

Get parliament information for a specific country.

* **Parameters:**
  **country_code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ISO 3166-1 alpha-3 country code (e.g., ‘FRA’, ‘GBR’, ‘USA’)
  or common name (e.g., ‘France’, ‘UK’)
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with parliament information

### Example

```pycon
>>> parliament = get_parliament('FRA')
>>> 'country' in parliament
True
>>>
>>> # Can also use country names
>>> parliament = get_parliament('France')
```

### elections.ipu_parline.get_women_in_parliament(country_code=None)

Get statistics on women in national parliaments.

* **Parameters:**
  **country_code** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional country code to filter by specific country
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with women in parliament statistics

### Example

```pycon
>>> stats = get_women_in_parliament()
>>> isinstance(stats, dict)
True
>>>
>>> # For specific country
>>> stats = get_women_in_parliament('SWE')
```

### elections.ipu_parline.search_parliaments(region=None, chamber_type=None)

Search for parliaments by region or chamber type.

* **Parameters:**
  * **region** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional region to filter (e.g., ‘Europe’, ‘Americas’, ‘Asia’)
  * **chamber_type** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional chamber type (‘bicameral’, ‘unicameral’)
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Returns:**
  List of parliament information

### Example

```pycon
>>> parliaments = search_parliaments(region='Europe')
>>> len(parliaments) > 0
True
```
