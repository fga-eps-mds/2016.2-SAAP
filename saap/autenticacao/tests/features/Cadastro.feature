Feature: Cadastro de Usuário
  To get acess to the saap features
  As an citizen 
  I want to register my self

  Scenario: Cadastre meu usuario
      Given I am on SAAP cadastro page
      And I type "gustavo" in the field "first_name"
      And I type "sabino" in the field "last_name"
      And I type "sabinogs" in the field "username"
      And I type "teste@teste.com" in the field "email"
      And I type "teste@teste.com" in the field "confirmacao_email"
      And I type "1234" in the field "password"
      And I type "1234" in the field "confirmacao_password"
      And I type "1996-01-07" in the field "data_de_nascimento"
      And I press "Selecionar"
      And I choose "Masculino"
      And I type "Guarulhos" in the field "municipio"
      And I press "UF"
      And I choose "SP"
      When I press "Enviar"
      Then I should see "Olá gustavo"
