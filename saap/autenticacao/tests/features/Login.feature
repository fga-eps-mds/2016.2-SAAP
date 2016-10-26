Feature: Login de Usuário
  To get acess to the saap features
  As an citizen
  I want to login my self

Scenario: Login valido
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "test_name"
        Then I fill in "password" with "123456"
        Then I press "Enviar"
        Then I should see "Olá test_name, seja bem vindo ao Sistema de Apoio à Atividade Parlamentar!"

Scenario: Login invalido
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "user_username"
        Then I fill in "password" with "invalid password"
        Then I press "Enviar"
        Then I should see "Nome de usuário e/ou senha inválido(s)!"

Scenario: Login invalido com campos em branco
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with ""
        Then I fill in "password" with ""
        Then I press "Enviar"
        Then I should see "O campo Nome de Usuário não foi preenchido!"

Scenario: Login invalido com nome de usuario em branco
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with ""
        Then I fill in "password" with "user_password"
        Then I press "Enviar"
        Then I should see "O campo Nome de Usuário não foi preenchido!"

Scenario: Login invalido com senha em branco
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "user_username"
        Then I fill in "password" with ""
        Then I press "Enviar"
        Then I should see "O campo Senha não foi preenchido!"
