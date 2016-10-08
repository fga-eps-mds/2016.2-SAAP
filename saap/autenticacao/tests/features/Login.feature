
Feature: Login de Usuário
  To get acess to the saap features
  As an citizen
  I want to login my self

Scenario: Login invalido
        When I visit site page "/login"
        Then I fill in "username" with "user_username"
        Then I fill in "password" with "user_password"
        Then I press "Enviar"
        Then I should see "Nome de usuário e/ou senha inválido(s)!"

Scenario: Login invalido com campos em branco
        When I visit site page "/login"
        Then I fill in "username" with ""
        Then I fill in "password" with ""
        Then I press "Enviar"
        Then I should see "Nome de usuário e/ou senha inválido(s)!"

Scenario: Login invalido com nome de usuario em branco
        When I visit site page "/login"
        Then I fill in "username" with ""
        Then I fill in "password" with "user_password"
        Then I press "Enviar"
        Then I should see "Nome de usuário e/ou senha inválido(s)!"

Scenario: Login invalido com senha em branco
        When I visit site page "/login"
        Then I fill in "username" with "user_username"
        Then I fill in "password" with "user_password"
        Then I press "Enviar"
        Then I should see "Nome de usuário e/ou senha inválido(s)!"
