'''
Conftest.py

Facilitates:
- URL customization through CLI and pytets.ini
- Launches playwright persistent contect based on browser-name
- resolves and sets delivery-date in URL
- sets output filename

'''


import pytest
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, VIEWPORT, LOCALE
from datetime import date, timedelta
import logging
from config.settings import UrlConfig, BASE_URL, USER_DATA_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#-------------------------
# PARAMETERIZING  URL
#-------------------------

def pytest_addoption(parser):
    parser.addini("modality", "Default modality")
    parser.addini("product", "Default product")
    parser.addini("data_mode", "Default data mode")
    parser.addini("market_area", "Default market_area")
    parser.addini("underlying_year", "Default underlying_year")
    parser.addini("sub_modality", "Default sub_modality")
    parser.addini("technology", "Default technology")
    parser.addini("period", "Default period")
    parser.addini("production_period", "Default production_period")
    parser.addini("auction", "Default auction")
    parser.addoption("--browser-name", action="store", default="chromium", help="Browser to run tests on: chromium/firefox/webkit")
    parser.addoption("--delivery-date", action="store", default=None)

@pytest.fixture(scope="session")
def url_config(request,resolve_date):
    return UrlConfig(
        modality=request.config.getini("modality"),
        product=request.config.getini("product"),
        data_mode=request.config.getini("data_mode"),
        market_area=request.config.getini("market_area"),
        underlying_year=request.config.getini("underlying_year"),
        sub_modality=request.config.getini("sub_modality"),
        technology=request.config.getini("technology"),
        period=request.config.getini("period"),
        production_period=request.config.getini("production_period"),
        auction=request.config.getini("auction"),
        delivery_date=resolve_date
    )

@pytest.fixture(scope="session")
def target_url(url_config):
    return url_config.build_url(BASE_URL)

#--------------------------------------------------------------------------
# Launch Browser, generate context and page objects, based on browser-name
#---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def page(request):
    with sync_playwright() as p:
        browser_name = request.config.getoption("--browser-name")
        if browser_name == "firefox":
            context = p.firefox.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=HEADLESS,
                viewport=VIEWPORT,
                locale=LOCALE,
            )
        elif browser_name == "chromium":
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=HEADLESS,
                viewport=VIEWPORT,
                locale=LOCALE,
            )
        elif browser_name == "webkit":
            context = p.webkit.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=HEADLESS,
                viewport=VIEWPORT,
                locale=LOCALE,
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        pg = context.pages[-1]  # avoid about:blank tab

        yield pg
        context.close()

#---------------------------------------------------------------------
# Set delivery-date parameter
#---------------------------------------------------------------------

@pytest.fixture(scope="session")
def resolve_date(request):
    """
       Resolve the delivery date for the EPEX SPOT query.
       Defaults to yesterday if no date provided.

       Args:
           date_arg: ISO date string e.g. '2026-03-19', or None.

       Returns:
           ISO format date string e.g. '2026-03-19'

       Raises:
           ValueError: If date_arg is not valid ISO format.
       """
    date_arg = request.config.getoption("--delivery-date")
    if date_arg:
        try:
            date.fromisoformat(date_arg)
        except ValueError:
            raise ValueError(
                f"Invalid date format: '{date_arg}'. "
                f"Expected ISO format e.g. '2026-03-19'."
            )
        logger.info(f"Using delivery date: {date_arg}")
        return date_arg

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    logger.info(f"No date provided — defaulting to yesterday: {yesterday}")
    return yesterday

#-------------------------------------------------------------------
# Set output filename
#-----------------------------------------------------------------------
@pytest.fixture(scope="session")
def output_path(resolve_date):
    import os
    os.makedirs("output", exist_ok=True)
    path = f"output/epex_{resolve_date}.csv"  # e.g. data/epex_GB_2026-03-21.csv
    yield path





