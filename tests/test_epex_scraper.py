"""
test_epex_scraper
"""

import os
import csv
import allure
import pytest
from datetime import date, timedelta

from pages.epex_market_page import EpexMarketPage
from utils.csv_writer import write_csv, HEADERS


EXPECTED_ROWS = 48
REQUIRED_COLS = ["Low", "High", "Last", "Weight Avg"]

#------------------------------------------------------------------
# Fixture to Naviagte to the site, Extract data and write to csv
#------------------------------------------------------------------
@pytest.fixture(scope="session")
def setup_data(page,resolve_date,output_path,target_url):

   #Get Page object
    mp = EpexMarketPage(page)

    # Navigate to the page
    mp.navigate_to_market(target_url)

    # ACCEPT COOKIES
    mp.accept_cookies()

    #Solve catcha manually (once per session)
    print("👉 Solve CAPTCHA if shown and wait for test to continue...")
    mp.wait_for_table()

    #Extract data from 4 target columns
    data = mp.extract_data()

    #Write to cvs file
    write_csv(data,output_path)

    print("CSV DATA WRITTEN")
    return {
        "page": page,
        "mp": mp,
        "data": data,
        "delivery-date":resolve_date,
        "output_path": output_path
    }

#---------------------------------------------------
# Test Class
#----------------------------------------------------

@allure.suite("EPEX SPOT Scraper")
@allure.feature("Market Data Scraping")
class TestMarketData:
    # -----------------------------
    # ✅ VALIDATE NAVIGATION
    # -----------------------------

    @allure.title("Navigation and page validation")
    def test_navigation(self, setup_data):
        page = setup_data["page"]
        delivery_date = setup_data["delivery-date"]

        url = page.url

        #Validate URL
        assert delivery_date in url
        assert "market-results" in url

        #validate reaching page with table
        assert page.locator("table.table-01").count() > 0
        assert page.locator("div.fixed-column li.sub-child.lvl-1").count() > 0

    # -----------------------------
    # ✅ DATA VALIDATION
    # -----------------------------



    @allure.title("Data extraction and validation")
    def test_data_extraction(self, setup_data):
        mp   = setup_data["mp"]
        data = setup_data["data"]

        col_map = mp.get_available_columns()

        for col in REQUIRED_COLS:
            assert col in col_map, f"Missing column: {col}"

        #validate all 48 data rows scraped
        assert len(data) == EXPECTED_ROWS
        for i, row in enumerate(data):
            #validate all 5 columns are present in each row
            assert len(row) == 5, f"Row {i}: expected 5 columns"

            #validate that no row has empty data
            assert all(cell.strip() for cell in row), f"Row {i}: empty value found — {row}"

            for val in row[1:]:
                v = val.strip()
                if v != "-":
                    float(v.replace(",", ""))  # raises ValueError if not numeric

    # -----------------------------
    # ✅ CSV VALIDATION
    # -----------------------------

    @allure.title("CSV output validation")
    def test_csv(self, setup_data):
        data = setup_data["data"]
        filename = setup_data["output_path"]

        # assert .csv file exits
        assert os.path.exists(filename)

        #assert file is not empty
        assert os.path.getsize(filename) > 0

        #assert all column names were written to csv file
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert reader.fieldnames == HEADERS

        assert len(rows) == len(data)

        #Validate no data-cell is empty
        empty_cells = [
            f"row {i+1} [{col}]"
            for i, row in enumerate(rows)
            for col, val in row.items()
            if not val.strip()
        ]
        assert not empty_cells
