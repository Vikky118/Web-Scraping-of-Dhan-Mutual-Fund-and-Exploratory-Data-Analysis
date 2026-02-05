"""import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clean(t):
    return " ".join(t.split()).strip() if t else None





driver = uc.Chrome()
driver.maximize_window()
driver.get("https://dhan.co/mutual-funds/all-mutual-funds/")

wait = WebDriverWait(driver, 20)
time.sleep(5)

data = []



def scroll_to_pagination():
    try:
        pagination = driver.find_element(By.CSS_SELECTOR, "nav[aria-label='pagination navigation']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pagination)
        time.sleep(1)
    except:
        pass


# --------------------------------
#      SCRAPE CURRENT PAGE
# --------------------------------
def scrape_current_page():
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    print("Rows found:", len(rows))

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")

        # FUND NAME
        try:
            name = clean(tds[0].find_element(By.TAG_NAME, "a").text)
        except:
            name = None

        # CATEGORY + TYPE
        tags = tds[0].find_elements(By.CSS_SELECTOR, "div.hidden.lg\\:flex p")
        category = clean(tags[0].text) if len(tags) > 0 else None
        type_ = clean(tags[1].text) if len(tags) > 1 else None

        # AUM
        aum = clean(tds[1].text)

        # RATING
        rating = clean(tds[2].text)

        # RETURNS
        r1 = clean(tds[3].text)
        r3 = clean(tds[4].text)
        r5 = clean(tds[5].text)

        # EXPENSE RATIO
        exp = clean(tds[6].text)

        data.append({
            "Fund Name": name,
            "Category": category,
            "Type": type_,
            "AUM": aum,
            "Rating": rating,
            "1Y Return": r1,
            "3Y Return": r3,
            "5Y Return": r5,
            "Expense Ratio": exp
        })


# --------------------------------
#   GO TO PAGE USING CORRECT SELECTOR
# --------------------------------
def go_to_page(page_number):

    scroll_to_pagination()

    print(f"Trying to click page {page_number}...")

    # Material UI uses aria-label="Go to page X"
    selector = f"button[aria-label='Go to page {page_number}']"

    btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )

    driver.execute_script("arguments[0].click();", btn)  # JS click for reliability
    time.sleep(3)  # wait for React to rerender


# --------------------------------
#   SCRAPE FIRST 5 PAGES
# --------------------------------

for page in range(1, 167):

    print(f"\n📌 SCRAPING PAGE {page}")
    time.sleep(2)

    scrape_current_page()

    if page < 166:
        go_to_page(page + 1)


driver.quit()

df = pd.DataFrame(data)
df.to_csv("dhan_mf_scraping.csv", index=False)
print("\n✅ Saved: dhan_mf_scraping.csv")
print(df)"""







import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# CLEAN FUNCTION

def clean(t):
    return " ".join(t.split()).strip() if t else None



# START SELENIUM

driver = uc.Chrome()
driver.maximize_window()
driver.get("https://dhan.co/mutual-funds/all-mutual-funds/")

wait = WebDriverWait(driver, 20)
time.sleep(6)

data = []


# SCROLL PAGINATION INTO VIEW

def scroll_to_pagination():
    try:
        pagination = driver.find_element(By.CSS_SELECTOR, "nav[aria-label='pagination navigation']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pagination)
        time.sleep(1)
    except:
        pass



# SCRAPE CURRENT PAGE

def scrape_current_page(page_no):
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    print(f"Rows on page {page_no}: {len(rows)}")

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")

        # FUND NAME
        name = clean(tds[0].find_element(By.TAG_NAME, "a").text)

        # CATEGORY + TYPE
        tags = tds[0].find_elements(By.CSS_SELECTOR, "div.hidden.lg\\:flex p")
        category = clean(tags[0].text) if len(tags) > 0 else None
        type_ = clean(tags[1].text) if len(tags) > 1 else None

        aum = clean(tds[1].text)
        rating = clean(tds[2].text)
        r1 = clean(tds[3].text)
        r3 = clean(tds[4].text)
        r5 = clean(tds[5].text)
        exp = clean(tds[6].text)

        data.append({
            "Page": page_no,
            "Fund Name": name,
            "Category": category,
            "Type": type_,
            "AUM": aum,
            "Rating": rating,
            "1Y Return": r1,
            "3Y Return": r3,
            "5Y Return": r5,
            "Expense Ratio": exp
        })



# CLICK PAGE USING FIRST FUND CHANGE DETECTION

def go_to_page(page_number):
    scroll_to_pagination()
    print(f"➡ Clicking page {page_number}...")

    # SELECTOR: visible button text
    xpath = f"//button[normalize-space()='{page_number}']"
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    # GET CURRENT FIRST FUND NAME (before clicking)
    try:
        old_name = driver.find_element(By.XPATH, "//table//tbody/tr[1]//a").text.strip()
    except:
        old_name = ""

    # CLICK BUTTON
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)

    # WAIT UNTIL FIRST FUND NAME CHANGES
    wait.until(
        lambda d: d.find_element(By.XPATH, "//table//tbody/tr[1]//a").text.strip() != old_name
    )

    time.sleep(0.5)   # small buffer



# MAIN LOOP — SCRAPE ALL 166 PAGES

TOTAL_PAGES = 166

for page in range(1, TOTAL_PAGES + 1):
    print(f"\n Scraping PAGE {page}/{TOTAL_PAGES}")
    scrape_current_page(page)

    if page < TOTAL_PAGES:
        go_to_page(page + 1)

driver.quit()



# SAVE RESULTS

df = pd.DataFrame(data)
df.to_csv("dhan_all_166_pages.csv", index=False)

print("\n DONE! Saved as dhan_all_pages.csv")
print(df.head())
print(f"\nTotal rows scraped: {len(df)}")


import os, subprocess
subprocess.Popen(r'explorer /select,"{}"'.format(os.path.abspath("dhan_all_pages.csv")))


