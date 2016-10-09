Feature: Cadastro de Usuário
  To get acess to the saap features
  As an citizen
  I want to password my self

  Scenario: Exclusão válida
          Given A user is registered
          When I visit site page "/login"
          Then I fill in "username" with "test_name"
          Then I fill in "password" with "123456"
          Then I press "Enviar"
          Then I press "Excluir Conta"
          Then I fill in "password" with "123456"
          Then I press "Enviar"
          Then I should see "Sua conta foi excluída"

Scenario: Exclusão invalida
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "test_name"
        Then I fill in "password" with "123456"
        Then I press "Enviar"
        Then I press "Excluir Conta"
        Then I fill in "password" with "12346"
        Then I press "Enviar"
        Then I should see "Senha incorreta"

Scenario: Exclusão com campo em branco
        Given A user is registered
        When I visit site page "/login"
        Then I fill in "username" with "test_name"
        Then I fill in "password" with "123456"
        Then I press "Enviar"
        Then I press "Excluir Conta"
        Then I fill in "password" with ""
        Then I press "Enviar"
        Then I should see "Senha incorreta"
