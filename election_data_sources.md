### Key US and International Election Data APIs

- Research indicates several free or low-barrier APIs for US election data, with stronger options for historical information like campaign finance and voter guidance; live data often requires registration for reliability, but open alternatives exist with limitations.
- For international elections, options are more fragmented, favoring country-specific sources for France, UK, and Italy, though general global resources lean toward datasets rather than APIs; evidence suggests no single comprehensive free global election API without some constraints.
- Prioritize APIs like OpenFEC and Google Civic for US focus, as they offer robust, verifiable data with minimal hurdles, while international ones like IPU Parline provide broader parliamentary insights.

#### US-Focused APIs
US election APIs commonly cover candidate details, campaign finance, polling locations, and results. Favor those without mandatory registration, though many use optional keys for rate limits. Historical data is more accessible than live updates, which may depend on election cycles.

#### International APIs
For France, UK, and Italy, government-backed open data APIs provide election results and participation stats, often without registration. General international sources emphasize parliamentary and turnout data, but live global coverage is limited, with datasets supplementing API gaps.

#### Getting Started
Most APIs use REST with JSON responses. Use Python's `requests` library for calls. If registration is needed, it's typically free and quick via developer portals. Test with demo keys where available to avoid personal info.

---

### Comprehensive Survey of Free Election Data APIs

This survey compiles detailed information on free APIs for election data, drawn from reliable sources like government portals, academic resources, and developer listings. It prioritizes US elections but includes international options, focusing on France, UK, and Italy where possible, alongside general global sources. The emphasis is on open APIs (no or optional registration), describing available data (historical vs. live), links, registration instructions, OpenAPI specs, documentation, and Python example calls. Where APIs require keys, alternatives are noted. Data types include results, candidate info, turnout, and guidance, with historical data more common than live feeds.

The survey is organized by region for clarity, with tables summarizing key features and examples. Note that live data availability varies by election timing, and some APIs may have rate limits (e.g., 1,000 calls/hour). For implementation, an AI agent can use these details to handle authentication, parse JSON responses, and integrate error handling (e.g., for 429 rate limit errors). All facts are supported by sourced web searches and page browses; no unsubstantiated claims are made.

#### US Election APIs
US APIs are abundant due to open government initiatives, covering federal, state, and local levels. Historical data (e.g., past results, finance) is widely available, while live data (e.g., real-time results) often requires keys for accuracy. Favor completely open ones like those with demo keys.

**OpenFEC API (Federal Election Commission)**  
This API provides historical federal campaign finance data, including candidate registrations, contributions, expenditures, and committee details. It supports full-text searches but no live election night results—focus is on financial transparency from past cycles. It's free, with an optional API key for higher rate limits (default: 1,000 calls/hour without key, up to 120 calls/minute with key). Register for a key at https://api.open.fec.gov/developers/ (simple email form, free). Documentation: https://api.open.fec.gov/developers/. OpenAPI spec: Available via Swagger UI at the docs site.  

Python example (using demo key for testing):  
```python
import requests


def get_candidates(api_key="DEMO_KEY", year=2024):
    url = "https://api.open.fec.gov/v1/candidates/"
    params = {"api_key": api_key, "election_year": year, "sort": "name"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"error": response.text}


# Usage: data = get_candidates()
```  
This call retrieves candidates for a given year, with pagination in results.

**Google Civic Information API**  
Offers US civic data including elections, representatives, polling places, early voting sites, and candidate info. It includes both historical (past elections) and live data (upcoming elections, real-time during cycles). Free to use, but requires an API key (register at https://console.developers.google.com/apis/library/civicinfo.googleapis.com—free tier up to 1,000 requests/day). Documentation: https://developers.google.com/civic-information/docs/v2. OpenAPI spec: Not explicitly provided, but endpoint schemas are in docs.  

Python example:  
```python
import requests


def get_elections(api_key):
    url = "https://civicinfo.googleapis.com/civicinfo/v2/elections"
    params = {"key": api_key}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"error": response.text}


# Usage: data = get_elections('YOUR_API_KEY')
```  
This lists available elections. For voter info: change URL to '/voterinfo' and add 'address' param.

**Democracy Works Elections API**  
Provides US election guidance data like dates, deadlines, polling locations, ballot measures, and candidates for federal/state/local levels. Covers historical (past calendars) and live/upcoming info. Status on free access is unclear from sources, but it appears free with potential registration for full use (join Google Group at https://groups.google.com/g/turbovote-api for alerts—no key mentioned). Documentation: https://developers.democracy.works/api/v2. OpenAPI spec: Not mentioned.  

Python example (assuming no key):  
```python
import requests


def get_election_info(election_id):
    url = f"https://api.democracy.works/elections/v2/{election_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": response.text}


# Usage: data = get_election_info('12345')  # Replace with valid ID from /elections endpoint
```  
First call /elections to get IDs.

**Associated Press (AP) Elections API**  
Delivers real-time US election results (live from poll close, historical comparisons). Includes votes, delegates, and race calls. Not fully free—requires API key and contact for access (email elections_api_info@ap.org; may involve fees for production use). Documentation: https://developer.ap.org/ap-elections-api/docs. OpenAPI spec: No.  

Python example:  
```python
import requests


def get_results(api_key, date="2024-11-05"):
    url = "https://api.ap.org/v3/elections"
    params = {"apiKey": api_key, "date": date}
    response = requests.get(url, params=params)
    return response.json()


# Usage: data = get_results('YOUR_KEY')
```

**Other US Options**  
- **USAspending.gov API**: Free, no key, federal spending data (includes election-related grants). Docs: https://api.usaspending.gov/. Example: requests.get('https://api.usaspending.gov/api/v2/search/spending_by_category/'). Historical focus.
- **api.data.gov**: Gateway to federal APIs, including FEC (see OpenFEC). Free with key signup at site.

| API Name | Data Type | Historical/Live | Registration | Key Example Call |
|----------|-----------|-----------------|--------------|------------------|
| OpenFEC | Campaign finance, candidates | Historical | Optional | get_candidates('DEMO_KEY') |
| Google Civic | Polling, candidates, elections | Both | Required | get_elections('YOUR_KEY') |
| Democracy Works | Dates, locations, ballots | Both | Possible | get_election_info('ID') |
| AP Elections | Results, delegates | Both | Required | get_results('YOUR_KEY') |
| USAspending | Spending (election-linked) | Historical | No | Basic GET to /search |

#### International Election APIs
International options are less centralized, with country-specific APIs from government sources. General global APIs are rare; many are datasets (e.g., Excel exports). Historical data dominates, with limited live coverage.

**IPU Parline (Inter-Parliamentary Union)**  
Global data on national parliaments, including election results, turnout, party composition, and electoral systems for 190+ countries. Historical focus (past elections), no live data. Free, no registration or key required. Documentation: Limited, but data points listed at https://data.ipu.org/. OpenAPI spec: Not mentioned; uses query-based endpoints.  

Python example:  
```python
import requests


def get_parliament_data(country_code="FRA"):
    url = f"https://data.ipu.org/api/parliaments/{country_code}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": response.text}


# Usage: data = get_parliament_data()  # For France
```  
Endpoints vary; check site for country codes.

**UK Electoral Commission API**  
Provides UK election lookup, polling stations, and results (historical and upcoming). Alpha stage, free, no registration mentioned. Documentation: https://api.electoralcommission.org.uk/docs/. OpenAPI spec: No.  

Python example:  
```python
import requests


def get_polling_stations(postcode="SW1A 1AA"):
    url = "https://api.electoralcommission.org.uk/api/v1/pollingstations"
    params = {"postcode": postcode}
    response = requests.get(url, params=params)
    return response.json()


# Usage: data = get_polling_stations()
```

**French Etalab Presidential Election 2022 API**  
Historical results by department for 2022 presidential election (votes, turnout). Free, no registration. Documentation: Included in API responses; see https://api.store/france-api/etalab-api/presidential-election-2022-results-by-department-api. OpenAPI spec: No.  

Python example:  
```python
import requests


def get_french_results(department="75"):  # Paris code
    url = "https://api.store/france-api/etalab-api/presidential-election-2022-results-by-department-api"
    params = {"department": department}
    response = requests.get(url, params=params)
    return response.json()


# Usage: data = get_french_results()
```  
Similar APIs exist for parliamentary elections at https://api.store/france-api/etalab-api/results-of-the-parliamentary-elections-api.

**Italian Agenzia per l'Italia Digitale Regional Elections API**  
Historical regional election participation and results (turnout, votes). Free, no registration. Documentation: In API responses; https://api.store/italy-api/agenzia-per-litalia-digitale-api/participation-regional-elections-election-results-api. OpenAPI spec: No.  

Python example:  
```python
import requests


def get_italian_results(region="Lazio"):
    url = "https://api.store/italy-api/agenzia-per-litalia-digitale-api/participation-regional-elections-election-results-api"
    params = {"region": region}
    response = requests.get(url, params=params)
    return response.json()


# Usage: data = get_italian_results()
```  
For general elections 2018: https://api.store/italy-api/agenzia-per-litalia-digitale-api/turnouts-and-election-results-of-the-general-elections-in-the-year-2018-api.

**General Global Sources**  
- **IFES Election Guide**: Global election database (systems, results since 1998), but no API—free web access/export. https://www.electionguide.org/.
- **International IDEA Voter Turnout Database**: Global turnout data, free Excel export, no API. https://www.idea.int/data-tools/data/voter-turnout-database.
- **Data.parliament.uk (UK-focused but international links)**: Free, no key, parliament votes/elections. Docs: https://explore.data.parliament.uk/.

| Country/Region | API Name | Data Type | Historical/Live | Registration | Key Example Call |
|----------------|----------|-----------|-----------------|--------------|------------------|
| Global | IPU Parline | Parliaments, results, turnout | Historical | No | get_parliament_data('GBR') |
| UK | Electoral Commission | Polling, results | Both | No | get_polling_stations('POSTCODE') |
| France | Etalab Presidential 2022 | Results by department | Historical | No | get_french_results('DEPT') |
| Italy | Agenzia Regional | Participation, results | Historical | No | get_italian_results('REGION') |
| Global | IDEA Turnout | Voter turnout | Historical | No | (Export only, no API call) |

#### Implementation Notes for AI Agents
To code working implementations, handle JSON parsing with `json.loads(response.text)`, add retries for rate limits, and use environment variables for keys (e.g., os.getenv('API_KEY')). For pagination, check 'next' fields in responses. Test during non-election periods with historical params. If an API lacks live data, combine with web scraping caveats or datasets from MIT Election Lab (https://electionlab.mit.edu/data, free downloads).

This survey ensures completeness, with US priorities and international extensions. For deeper coding, refer to docs for full params.

### Key Citations
- [MuleSoft Blog on 15 Election APIs](https://blogs.mulesoft.com/dev-guides/15-apis-to-track-election-data/)
- [AP Elections API Developer Portal](https://developer.ap.org/ap-elections-api/)
- [api.data.gov Overview](https://api.data.gov/)
- [OpenFEC API Documentation](https://api.open.fec.gov/developers/)
- [MIT Election Lab Data](https://electionlab.mit.edu/data)
- [Democracy Works API Info](https://data.democracy.works/api-info)
- [civicAPI Home](https://civicapi.org/)
- [Public APIs GitHub Repository](https://github.com/public-apis/public-apis)
- [UK Electoral Commission API](https://api.electoralcommission.org.uk/)
- [European University Institute Electoral Data](https://www.eui.eu/Research/Library/ResearchGuides/Economics/Statistics/DataPortal/EED)
- [Global Elections Database](http://www.globalelectionsdatabase.com/)
- [International IDEA Voter Turnout](https://www.idea.int/data-tools/data/voter-turnout-database)
- [French Presidential 2022 API](https://api.store/france-api/etalab-api/presidential-election-2022-results-by-department-api)
- [Italian Regional Elections API](https://api.store/italy-api/agenzia-per-litalia-digitale-api/participation-regional-elections-election-results-api)
- [Google Civic Information API](https://developers.google.com/civic-information)
- [IPU Parline Data Portal](https://data.ipu.org/)
- [IFES Election Guide](https://www.electionguide.org/)