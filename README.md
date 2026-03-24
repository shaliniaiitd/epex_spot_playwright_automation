# EPEX SPOT Market Scraper Test

Playwright-based automated test that scrapes half-hourly market data (Low, High, Last, Weight Avg) from the EPEX SPOT GB Continuous market results page and writes it to a CSV file.

## PROJECT STRUCTURE

.epex_spot
|__.github             # CI/CD workflow
├── pages/             # Page Object Model classes
├── tests/             # Test suite
├── utils/             # Utilities (CSV writer)
├── config/            # Configuration settings
├── conftest.py        # Pytest fixtures
├── pytest.ini         # Default parameters
└── README.md


## SETUP

pip install -r requirements.txt
playwright install


## RUN
> Note: End-to-end scraping requires manual CAPTCHA resolution on first run.
# Default (Chromium)
pytest -s

# Specific browser
pytest -s --browser-name=firefox
pytest -s --browser-name=webkit

# For a spedific delivery date(ISO Format)
pytest -s --delivery-date=2026-03-19

# With Allure report
pytest -s --alluredir=allure-results
allure serve allure-results
```bash

## CAPTCHA

EPEX SPOT uses Cloudflare bot protection. 
If CAPTCHA is triggered, it must be solved manually during the first run. 
A persistent browser session (`session/` folder) is used to reduce repeated challenges.

## DESIGN NOTES

**Dynamic column detection** — column positions are read from table headers at runtime rather than hardcoded. If EPEX SPOT reorders columns the scraper still extracts the correct data.

**Cross-browser** — pass `--browser-name=firefox` or `--browser-name=webkit` to run on a different browser.

**DESIGN PATTERNS** - Page object and template method have been implemented in test framework design.

**Allure reporting**
Allure can be used for test reporting if installed locally.


## CONFIGURATION

The test is fully configurable via both CLI and `pytest.ini`.

# CLI Parameters

`--delivery-date` → specify delivery date (ISO format: YYYY-MM-DD)
 --browser-name` → choose browser (chromium / firefox / webkit)

Example:
pytest -s --delivery-date=2026-03-19 --browser-name=firefox

# pytest.ini Configuration

Default URL parameters (market, modality, product, etc.) are defined in pytest.ini.

This allows:

easy switching of markets or products
reuse across different test scenarios
separation of test logic from configuration

The final URL is dynamically constructed using CLI inputs and configuration values.

## ERROR HANDLING
Following errors are addressed:
- Unsupported browser name specified
- missing headers and DOM inconsistencies
- Required columns not found on page
- No data rows found
- Mismatch between hour labels and data rows
- Non-numeric data values encountered
- delivery-date not in iso format 
- Invalid delivery date format (expected ISO format)

## TEST COVERAGE
Pytest framework has been used for following validations.

**test_navigation**
- Correct page is loaded
- Results table is visible

**test_data_extraction**
- Required columns are present
- Expected number of rows (48) is fetched
- Data values are numeric
- No empty cells

**test_csv**
- Output file exists
- File is not empty
- Headers match expected values
- Row count matches extracted data
- No empty values in CSV

## CI / AUTOMATION

## CI / Automation

A GitHub Actions workflow is included to validate the project setup.

- Runs on Ubuntu with Python 3.11
- Installs dependencies and Playwright

Note:
End-to-end scraping tests are not executed in CI due to Cloudflare CAPTCHA and session requirements. 
They are intended to be run locally.


## ASSUMPTIONS

- Market selected: GB Continuous
- Data is expected in 30-minute intervals (48 rows per day)
- Placeholder rows (hour aggregates) are excluded from scraping
- CAPTCHA may appear on first run and requires manual resolution

## POSSIBLE IMPROVEMENTS

- Fully automated CAPTCHA handling (if supported by test environment)
- API-based data extraction (if available)
- Retry and resilience mechanisms for flaky UI loads
- Parallel test execution across browsers

