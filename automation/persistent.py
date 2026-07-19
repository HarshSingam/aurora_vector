from automation.browser import open_browser

def open_persistent():
    playwright , browser , page = open_browser()

    page.goto(
    "https://careers.persistent.com/",
    wait_until="domcontentloaded",
    timeout=60000
    )

   #page.pause()
    
    print("Title :", page.title())
    print("URL   :", page.url)
#counting links 
    
    # buttons= page.locator("button")
    # print("Number of buttons:", buttons.count())

    # inputs = page.locator("input")

    # print("Total inputs:", inputs.count())

    # for i in range(inputs.count()):
        # print("----------------")
        # print("Input", i + 1)
        # print("Placeholder:", inputs.nth(i).get_attribute("placeholder"))
        # print("ID:", inputs.nth(i).get_attribute("id"))
        # print("Type:", inputs.nth(i).get_attribute("type"))
        # print("TestID:", inputs.nth(i).get_attribute("data-testid"))

    search_box = page.get_by_role("textbox",
        name="Search by role or keyword...")
    
    search_box.wait_for(state="visible", timeout=60000)
    print("Search box found:", search_box.count())

    search_box.click()

    search_box.type("python developer" , delay=100)

    print("Typed:", search_box.input_value())

    search_box.press("Enter")

    india_checkbox = page.get_by_role("checkbox", name="India")
    india_checkbox.wait_for(timeout=6000)
    india_checkbox.check()
    page.wait_for_timeout(3000)
    print(india_checkbox.is_checked())


    job_cards = page.locator("lib-job")

    for i in range(job_cards.count()):

        card = job_cards.nth(i)

        title = card.locator("mat-card-title").inner_text()

        location = card.locator(".fw-bold").inner_text()

        skills = []

        skill_locator = card.locator("mat-chip")

        for j in range(skill_locator.count()):
            skills.append(
                skill_locator.nth(j).inner_text()
            )

        print("=" * 40)
        print(title)
        print(location)
        print(skills)


    input("Press Enter to close...")

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    open_persistent()
