from automation.browser import open_browser

def open_persistent():
    playwright , browser , page = open_browser()

    page.goto(
        "https://careers.persistent.com/",
        wait_until="networkidle"
    )

    print(page.title())

    input("Press Enter to close...")

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    open_persistent()