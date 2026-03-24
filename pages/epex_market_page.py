from pages.base_page import BasePage
from config.settings import (
    TABLE_SELECTOR, HOUR_SELECTOR, ROW_SELECTOR,
    HEADER_SELECTOR, COOKIE_SELECTOR, TABLE_TIMEOUT_MS,
    CAPTCHA_WAIT_MS, COL_LOW, COL_HIGH, COL_LAST, COL_WEIGHT_AVG
)


class EpexMarketPage(BasePage):
    """
       Page Object for EPEX SPOT market results.

       Responsibilities:
       -Navigate to generated  URL
       - Handle cookie consent banner (inherited from BasePage)
       - Wait for dynamic table to finish loading
       - Detect column positions dynamically from table headers
       - Scrape and return structured half-hour market data rows

       """

    # ----------------------------------------------------------
    #Navigate to generated  URL
    # ----------------------------------------------------------
    def navigate_to_market(self, target_url):
        self.navigate(target_url)

    # ----------------------------------------------------------
    # Wait for dynamic table to finish loading
    # ----------------------------------------------------------
    def wait_for_table(self):
        # Give time for manual CAPTCHA resolution (if present)
        self.page.wait_for_timeout(CAPTCHA_WAIT_MS)
        try:
            self.page.locator(TABLE_SELECTOR).wait_for(
                state="visible", timeout=TABLE_TIMEOUT_MS
            )
        except Exception:
            raise TimeoutError("Results table did not load within expected time.")

    # ----------------------------------------------------------
    # Detect column positions dynamically from table headers
    # ----------------------------------------------------------
    def _get_column_map(self):
        headers = self.page.locator(HEADER_SELECTOR)
        col_map = {}
        headers_count = headers.count()

        if headers.count() == 0:
            raise ValueError("Table headers not found — page structure may have changed.")

        for i in range(headers_count):
            text = headers.nth(i).inner_text().replace("\n", " ").strip()
            if text.startswith("Low"):       col_map[COL_LOW] = i
            elif text.startswith("High"):    col_map[COL_HIGH] = i
            elif text.startswith("Last"):    col_map[COL_LAST] = i
            elif text.startswith("Weight"):   col_map[COL_WEIGHT_AVG] = i
        missing = [c for c in [COL_LOW, COL_HIGH, COL_LAST, COL_WEIGHT_AVG] if c not in col_map]
        if missing:
            raise ValueError(f"Required columns not found: {missing}")
        return col_map

    # get list of columns for which data is to be scraped
    def get_available_columns(self):
        return list(self._get_column_map().keys())

    #----------------------------------------------------------
    # Scrape and return structured half-hour market data rows
    #----------------------------------------------------------
    def get_hours(self):
        hours = self.page.locator(HOUR_SELECTOR)
        count = hours.count()
        return [hours.nth(i).inner_text().strip()
                for i in range(count)]

    def extract_data(self):
        col_map = self._get_column_map()
        rows = self.page.locator(ROW_SELECTOR)
        hours = self.get_hours()

        row_count = rows.count()

        if row_count == 0:
            raise ValueError("No data rows found — page may not have loaded.")
        if len(hours) != row_count:
            raise ValueError(
                f"Mismatch: {len(hours)} hour labels, {row_count} data rows."
            )

        data = []
        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            data.append([
                hours[i],
                cells.nth(col_map[COL_LOW]).inner_text().strip(),
                cells.nth(col_map[COL_HIGH]).inner_text().strip(),
                cells.nth(col_map[COL_LAST]).inner_text().strip(),
                cells.nth(col_map[COL_WEIGHT_AVG]).inner_text().strip(),
            ])
        return data
