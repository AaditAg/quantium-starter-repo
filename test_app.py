import time
import pytest
from dash import dcc, html
from dash import Dash
from visualisation import app
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('http://localhost:8050/')  # Adjust the URL if your Dash app runs on a different port
    time.sleep(5)  # Let the page load
    yield driver
    driver.quit()

def test_header_present(driver):
    header = driver.find_element(By.TAG_NAME, 'h1')
    assert header is not None
    assert 'Sales Data for Pink Morsel' in header.text

def test_graph_present(driver):
    graph = driver.find_element(By.CSS_SELECTOR, '#sales-bar-chart')
    assert graph is not None

def test_radio_buttons_present(driver):
    radio_items = driver.find_element(By.CSS_SELECTOR, '#region-selector')
    assert radio_items is not None
    options = radio_items.find_elements(By.TAG_NAME, 'input')
    assert len(options) == 5

def test_initial_graph_data(driver):
    graph = driver.find_element(By.CSS_SELECTOR, '#sales-bar-chart')
    assert graph is not None

def test_initial_table_data(driver):
    table = driver.find_element(By.CSS_SELECTOR, '#sales-table')
    assert table is not None
    rows = table.find_elements(By.TAG_NAME, 'tr')
    assert len(rows) > 0
