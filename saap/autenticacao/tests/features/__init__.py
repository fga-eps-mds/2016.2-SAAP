# -*- coding: utf-8 -*-
from aloe import step, world
import aloe_webdriver
from contextlib import contextmanager

import aloe_webdriver
import aloe_webdriver.django
from aloe import around, world, step
from selenium import webdriver
from selenium.webdriver.support.ui import Select

@around.each_example
@contextmanager
def with_browser(scenario,outline,steps):
    world.browser = webdriver.Chrome()
    yield  
    world.browser.quit()
    delattr(world,'browser')


@step(r'I click in "(.*)"')
def click(scenario, link):
  world.browser.find_element_by_link_text(link).click()

@step(r'I select "(.*)" from "(.*)"')
def multiselect_set_selections(driver, labels, element_id):
   # el = driver.find_element_by_id(element_id)
    el = world.browser.find_element_by_id(element_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text in labels:
            option.click()

#@step(r'I select "(.*)" from "(.*)"')
#def select(scenario, text, select_id):
#  print(80*"-")
#  print("")
#  print(80*"-")
#  select = Select(world.browser.find_element_by_id(select_id))
#  select.select_by_visible_text(text)

@step(r'I access "(.*)"')
def access_url(step,url):
    world.fb = url

@step(r'Given I am on SAAP cadastro page')
def given_i_am_on_saap_cadastro_page(step):
    full_url = django.django_url('cadastro')
    world.browser.get(full_url)

@step(u'And I type "([^"]*)" in the field "([^"]*)"')
def and_i_type_group1_in_the_field_group2(step, group1, group2):
    assert False, 'This step must be implemented'

@step(u'And I press "([^"]*)"')
def and_i_press_group1(step, group1):
    assert False, 'This step must be implemented'

@step(u'And I choose "([^"]*)"')
def and_i_choose_group1(step, group1):
    assert False, 'This step must be implemented'

@step(u'When I press "([^"]*)"')
def when_i_press_group1(step, group1):
    assert False, 'This step must be implemented'

@step(u'Then I should see "([^"]*)"')
def then_i_should_see_group1(step, group1):
    assert False, 'This step must be implemented'

