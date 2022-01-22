from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


def scrape_detail_page(driver: webdriver.Chrome):
    product = {}
    specs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.d-flex.justify-content-between.align-items-center.product-specs.px-0.px-md-16px"))
    )
    product["name"] = driver.find_element(By.CSS_SELECTOR, "div.product-details-content div.pd-title h1").text
    product["price"] = driver.find_element(By.CSS_SELECTOR, "div.product-details-content > div.buy-section > div.text-center > div > div.pr-price").text

    for spec in specs:
        product[spec.find_element(By.TAG_NAME, "span").text] = [spec.find_element(By.TAG_NAME, "p").text]

    return pd.DataFrame(product)


def main(url, category, sub_category, brand, condition, page=1):
    driver = webdriver.Chrome()
    _url = url.format(cat = category, subcat=sub_category, brand=brand, condition=condition, page=page)
    driver.get(_url)

    wait = WebDriverWait(driver, 20)

    pagination = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li > a.pagination-link')))
    total_pagination = int(pagination[-2].text)

    data = pd.DataFrame()
    for i in range(total_pagination):
        print(f"Page: {i+1}")
        product_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-content-cards.mx-0.mx-lg-n8px.flex-1.row'))
        )
        links = product_container.find_elements(By.CSS_SELECTOR, 'div.card-col a.d-block.text-decoration-none')
        current = 0
        while current < len(links):
            print(f"---- product {current+1}")
            driver.execute_script("arguments[0].click();", links[current])

            data = data.append(scrape_detail_page(driver))

            driver.execute_script("window.history.go(-1)")
            current += 1

            product_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-content-cards.mx-0.mx-lg-n8px.flex-1.row'))
            )
            links = product_container.find_elements(By.CSS_SELECTOR, 'div.card-col a.d-block.text-decoration-none')

        data.to_csv("datasets/data.csv", index=False)

        next_button = product_container.find_element(By.CSS_SELECTOR, 'a.pagination-link.pagination-arrow.pagination-next')
        driver.execute_script("arguments[0].click();", next_button)


if __name__ == "__main__":
    url = "https://www.mymarket.ge/en/search/{cat}/{subcat}/?Brands={brand}&CatID={cat}&CondTypeID={condition}&Page={page}"
    main(url, 69, "Mobile-Phones", 42, 0)
