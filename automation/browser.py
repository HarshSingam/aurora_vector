from playwright.sync_api import sync_playwright


def open_browser():
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page = browser.new_page()

    return playwright, browser, page