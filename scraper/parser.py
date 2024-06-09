from selenium import webdriver
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


async def get_schedule(settlement: str):
    url = 'https://energy.volyn.ua/spozhyvacham/perervy-u-elektropostachanni/hrafik-vidkliuchen/#gsc.tab=0'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    await asyncio.sleep(5)
    form_city = driver.find_element(By.ID, 'formCity')
    form_city.send_keys(settlement)

    form_city.send_keys(Keys.RETURN)
    await asyncio.sleep(5)
    try:
        schedule_item = driver.find_element(By.CSS_SELECTOR, '.table.table-sm.table-light.table-hover.text-wrap.fs-9')
    except Exception as ex:
        print("Нас. пункт не найдено!")
        return
    schedule_html_outer = schedule_item.get_attribute('outerHTML')
    data_schedule = await parse_schedule(schedule_html_outer)

    driver.quit()

    return data_schedule


async def parse_schedule(html):
    soup = BeautifulSoup(html, 'html.parser')

    data = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        region = columns[0].text
        settlement = columns[1].text
        street = columns[2].text
        houses = columns[3].text
        queue = columns[4].text
        date = columns[5].text
        hours = columns[6].text

        data.append({
            'region': region,
            'settlement': settlement,
            'street': street,
            'houses': houses,
            'queue': queue,
            'date': date,
            'hours': hours

        })

    return data
