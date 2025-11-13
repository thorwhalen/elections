"""Election Data Package

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

    >>> from elections import ElectionsDataGetters
    >>>
    >>> # Access all data sources as a mapping
    >>> getters = ElectionsDataGetters()
    >>> list(getters.keys())  # doctest: +SKIP
    ['nytimes', 'openfec', 'google_civic', 'democracy_works', 'ipu_parline']
    >>>
    >>> # Access a specific data source module
    >>> nyt = getters['nytimes']  # doctest: +SKIP
    >>> data = nyt.get_election_data('florida', year=2020)  # doctest: +SKIP
    >>>
    >>> # Or import modules directly
    >>> from elections import nytimes
    >>> data = nytimes.get_election_data('pennsylvania', year=2020)  # doctest: +SKIP

**Consistent Parameter Names:**

Across all modules, we use consistent parameter names for common concepts:

- **year**: Election year (e.g., 2020, 2024)
- **region**: Geographic region (state abbreviation like 'PA', or state name like 'pennsylvania')
- **api_key**: API authentication key (when required)
- **race_type**: Type of race (e.g., 'president', 'senate', 'house')
- **office**: Office being sought (used by some APIs)

**API Keys:**

Some data sources require API keys:

- **openfec**: Optional (use 'DEMO_KEY' or get free key at https://api.open.fec.gov/developers/)
- **google_civic**: Required (get free key at https://console.developers.google.com/)
- **democracy_works**: Not required
- **nytimes**: Not required
- **ipu_parline**: Not required

Set API keys via environment variables:
- OPENFEC_API_KEY
- GOOGLE_CIVIC_API_KEY

**Example Workflows:**

Get NYT election results for multiple states:

    >>> from elections.nytimes import get_election_data
    >>> states = ['florida', 'pennsylvania', 'georgia']
    >>> results = {s: get_election_data(s, year=2020) for s in states}  # doctest: +SKIP

Search for campaign finance data:

    >>> from elections.openfec import search_candidates, get_candidate_totals
    >>> candidates = search_candidates('Biden', year=2024)  # doctest: +SKIP
    >>> # Get financial totals for specific candidate
    >>> totals = get_candidate_totals('P80001571', year=2020)  # doctest: +SKIP

Get voter information for an address:

    >>> from elections.google_civic import get_voter_info
    >>> info = get_voter_info(  # doctest: +SKIP
    ...     '1600 Pennsylvania Ave NW, Washington, DC 20500',
    ...     api_key='YOUR_KEY'
    ... )

Get international election data:

    >>> from elections.ipu_parline import get_parliament, get_election_results
    >>> france = get_parliament('FRA')  # doctest: +SKIP
    >>> results = get_election_results('DEU')  # doctest: +SKIP

"""

from collections.abc import Mapping
from typing import Any, Iterator
import importlib


# Backward compatibility - import classes from nytimes module (if available)
try:
    from elections.nytimes import (
        Election2020RawJson,
        Races2020,
        President2020TimeSeries,
    )
except ImportError as e:
    # If py2store or pandas not available, skip backward compatibility imports
    Election2020RawJson = None
    Races2020 = None
    President2020TimeSeries = None


class ElectionsDataGetters(Mapping):
    """
    Mapping interface to election data sources.

    This class provides dict-like access to different election data source modules.
    Each key is a source identifier, and the value is the corresponding module.

    **Available Sources:**

    - 'nytimes': New York Times election results API
    - 'openfec': Federal Election Commission API
    - 'google_civic': Google Civic Information API
    - 'democracy_works': Democracy Works Elections API
    - 'ipu_parline': Inter-Parliamentary Union Parline database

    **Usage:**

        >>> getters = ElectionsDataGetters()
        >>>
        >>> # List all available sources
        >>> sources = list(getters.keys())  # doctest: +SKIP
        >>>
        >>> # Access a specific source
        >>> nyt_module = getters['nytimes']  # doctest: +SKIP
        >>> data = nyt_module.get_election_data('florida', year=2020)  # doctest: +SKIP
        >>>
        >>> # Iterate over all sources
        >>> for source_id, module in getters.items():  # doctest: +SKIP
        ...     print(f"{source_id}: {module.__doc__.split(chr(10))[0]}")
        >>>
        >>> # Check if a source exists
        >>> 'nytimes' in getters  # doctest: +SKIP
        True

    **Attributes:**

    Each source module provides its own functions and classes for accessing data.
    See the module documentation for details:

        >>> getters = ElectionsDataGetters()
        >>> nyt = getters['nytimes']  # doctest: +SKIP
        >>> help(nyt)  # doctest: +SKIP
    """

    _sources = {
        'nytimes': 'elections.nytimes',
        'openfec': 'elections.openfec',
        'google_civic': 'elections.google_civic',
        'democracy_works': 'elections.democracy_works',
        'ipu_parline': 'elections.ipu_parline',
    }

    def __init__(self):
        """Initialize the ElectionsDataGetters mapping."""
        self._modules = {}

    def __getitem__(self, key: str) -> Any:
        """
        Get a data source module by its identifier.

        Args:
            key: Source identifier (e.g., 'nytimes', 'openfec')

        Returns:
            The imported module for that data source

        Raises:
            KeyError: If the source identifier is not recognized
            ImportError: If the module cannot be imported (e.g., missing dependencies)
        """
        if key not in self._sources:
            raise KeyError(
                f"Unknown data source: {key}. "
                f"Available sources: {list(self._sources.keys())}"
            )

        # Lazy load modules
        if key not in self._modules:
            module_path = self._sources[key]
            try:
                self._modules[key] = importlib.import_module(module_path)
            except ImportError as e:
                raise ImportError(
                    f"Cannot import {key} module: {e}. "
                    f"This may be due to missing dependencies. "
                    f"For 'nytimes', ensure 'py2store' and 'pandas' are installed."
                ) from e

        return self._modules[key]

    def __iter__(self) -> Iterator[str]:
        """Iterate over source identifiers."""
        return iter(self._sources)

    def __len__(self) -> int:
        """Return the number of available data sources."""
        return len(self._sources)

    def __repr__(self) -> str:
        """Return a string representation of available sources."""
        return f"ElectionsDataGetters({list(self._sources.keys())})"

    def describe(self) -> None:
        """
        Print descriptions of all available data sources.

        This method loads each module and prints its first docstring line
        along with key information about the data source.
        """
        print("Available Election Data Sources:")
        print("=" * 80)

        for source_id in self._sources:
            module = self[source_id]
            # Get first line of module docstring
            doc_lines = module.__doc__.split('\n') if module.__doc__ else []
            first_line = next((line.strip() for line in doc_lines if line.strip()), 'No description')

            print(f"\n{source_id}:")
            print(f"  {first_line}")

            # Try to extract key info from docstring
            if module.__doc__:
                for line in doc_lines:
                    if 'Access:' in line or 'API Key' in line or 'Coverage:' in line:
                        print(f"  {line.strip()}")


# Convenience: pre-instantiate a default getter
_default_getters = ElectionsDataGetters()


def get_source(source_id: str) -> Any:
    """
    Convenience function to get a data source module.

    Args:
        source_id: Source identifier (e.g., 'nytimes', 'openfec')

    Returns:
        The data source module

    Example:
        >>> from elections import get_source
        >>> nyt = get_source('nytimes')  # doctest: +SKIP
        >>> data = nyt.get_election_data('florida', year=2020)  # doctest: +SKIP
    """
    return _default_getters[source_id]


def list_sources() -> list:
    """
    List all available data source identifiers.

    Returns:
        List of source identifier strings

    Example:
        >>> from elections import list_sources
        >>> sources = list_sources()
        >>> 'nytimes' in sources
        True
        >>> 'openfec' in sources
        True
    """
    return list(_default_getters.keys())


# Export main classes and functions
__all__ = [
    'ElectionsDataGetters',
    'get_source',
    'list_sources',
    # Backward compatibility exports
    'Election2020RawJson',
    'Races2020',
    'President2020TimeSeries',
]
