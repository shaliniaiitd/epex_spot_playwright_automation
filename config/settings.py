"""
config/settings.py
------------------
Central configuration for the EPEX SPOT scraper..
"""
from dataclasses import dataclass
from urllib.parse import urlencode

#------------------
# BUILD URL
#------------------

BASE_URL    = "https://www.epexspot.com/en/market-results"


@dataclass
class UrlConfig:
    modality: str
    product: str
    data_mode: str
    market_area: str
    underlying_year: str
    sub_modality: str
    technology: str
    period: str
    production_period: str
    delivery_date: str  # ISO format YYYY-MM-DD
    auction: str

    def build_url(self, base_url: str=BASE_URL) -> str:
        params = {
            "modality": self.modality,
            "product": self.product,
            "data_mode": self.data_mode,
            "market_area": self.market_area,
            "underlying_year": self.underlying_year,
            "sub_modality":self.sub_modality,
            "technology":self.technology,
            "period": self.period,
            "production_period":self.production_period,
            "delivery_date": self.delivery_date,
            "auction": self.auction
        }
        params = {k: v for k, v in params.items() if v}
        return f"{base_url}?{urlencode(params)}"

#--------------------
# BROWSER SETTINGS
#--------------------

USER_DATA_DIR = "session"        # folder where Chrome session is persisted
HEADLESS      = False
VIEWPORT      = {"width": 1280, "height": 900}
LOCALE        = "en-GB"

#--------------------
# Timeouts (milliseconds)
#--------------------

TABLE_TIMEOUT_MS   = 15_000      # wait for results table
COOKIE_TIMEOUT_MS  = 3_000       # cookie banner may not always appear
CAPTCHA_WAIT_MS    = 3_000       # grace period for manual CAPTCHA solving

#--------------------
# SELECTORS
#---------------------

# Hour labels live in a fixed left-column list separate from the data table.
# Confirmed by DOM inspection — both collections share the same order and count.
HOUR_SELECTOR   = "div.fixed-column li.sub-child.lvl-1"
ROW_SELECTOR    = "table.table-01 tbody > tr.lvl-1"
TABLE_SELECTOR  = "table.table-01"
HEADER_SELECTOR = "table.table-01 thead th"
COOKIE_SELECTOR = "button.agree-button"  # confirmed by DOM inspection

#--------------------
#  COLUMN NAMES
# -------------------
# Names of columns from which data is to be scraped.

COL_LOW         = "Low"
COL_HIGH        = "High"
COL_LAST        = "Last"
COL_WEIGHT_AVG  = "Weight Avg"



