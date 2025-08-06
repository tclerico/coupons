import os
import time

from playwright.sync_api import sync_playwright, Playwright

tag_selector = """
    {
      query(root, selector) {
        return root.querySelector(selector);
      },

      queryAll(root, selector) {
        return Array.from(root.querySelectorAll(selector));
      }
    }"""

def run(playwright: Playwright):
    url = "https://www.wegmans.com/"
    coupon_url = "https://www.wegmans.com/shop/coupons"
    username = os.environ.get('username')
    password = os.environ.get('password')
    
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    
    playwright.selectors.register("tag", tag_selector)
    page.locator("tag=span").get_by_text("Sign In / Register").click()
    
    page.locator("id=signInName").wait_for()
    page.locator("id=signInName").type(username)
    page.locator("id=password").type(password)
    page.locator("id=next").click()
    
    page.locator("css=.component--site-header-desktop-subnav-presentation").wait_for()
    
    page.goto(coupon_url)
    page.locator("css=.component--coupons-landing-page-grid").wait_for()
    
    # this can probably be workshopped
    scroll_depth = 6
    for i in range(scroll_depth):
        page.locator("tag=footer").scroll_into_view_if_needed()
    
    to_clip = page.locator("css=.clip-button").all()
    for button in to_clip:
        button.click()
        time.sleep(2)
    


if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(playwright)