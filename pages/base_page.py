from config.settings import COOKIE_SELECTOR
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page:Page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url, wait_until="domcontentloaded")

    # Handle cookie consent banner
    def accept_cookies(self):
        btn = self.page.locator(COOKIE_SELECTOR)
        try:
            btn.wait_for(state="visible", timeout=3000)
            btn.click()
        except Exception as e:
            print(f"Cookie handling skipped: {e}")

