Feature: Cadastro de Usuário
  To get acess to the saap features
  As an citizen
  I want to password my self

Scenario: Mudança valida
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "test_name"
        Then I fill in "password" with "123456"
        Then I press "Enviar"
        When I visit site page "/mudar_senha"
        Then I fill in "nova_senha" with "234567"
        Then I fill in "confirmacao_nova_senha" with "234567"
        Then I press "Enviar"
        Then I should see "Seja Bem vindo a o SAAP"

Scenario: Mudança invalida
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "test_name"
        Then I fill in "password" with "123456"
        Then I press "Enviar"
        When I visit site page "/mudar_senha"
        Then I fill in "nova_senha" with "234567"
        Then I fill in "confirmacao_nova_senha" with "234568"
        Then I press "Enviar"
        Then I should see "Seja Bem vindo a o SAAP"
        
