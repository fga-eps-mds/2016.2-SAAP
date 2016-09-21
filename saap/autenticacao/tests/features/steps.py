# -*- coding: utf-8 -*-
from lettuce import step, before, world
from splinter.browser import Browser
from lettuce import django

@before.all
def set_browser():
	world.browser = Browser('firefox')

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
