from contextlib import contextmanager

import aloe_webdriver
import aloe_webdriver.django
from aloe import around, world, step
from selenium import webdriver
from selenium.webdriver.support.ui import Select

@around.each_example
@contextmanager
def with_browser(scenario,outline,steps):
    world.browser = webdriver.Firefox()
    yield  
    world.browser.quit()
    delattr(world,'browser')  


@step(r'I click in "(.*)"')
def click(scenario, link):
  world.browser.find_element_by_link_text(link).click()

@step(r'I select "(.*)" from "(.*)"')
def select(scenario, text, select_id):
  select = Select(world.browser.find_element_by_id(select_id))
  select.select_by_visible_text(text)
