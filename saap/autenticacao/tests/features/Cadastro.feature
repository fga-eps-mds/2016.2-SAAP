Feature: Cadastro de Usuário
  To get acess to the saap features
  As an citizen 
  I want to register my self

  #  Scenario: Cadastre meu usuario
  #      Given I acces 
  #      And I type "gustavo" in the field "first_name"
  #      And I type "sabino" in the field "last_name"
  #      And I type "sabinogs" in the field "username"
  #      And I type "teste@teste.com" in the field "email"
  #      And I type "teste@teste.com" in the field "confirmacao_email"
  #      And I type "1234" in the field "password"
  #      And I type "1234" in the field "confirmacao_password"
  #      And I type "1996-01-07" in the field "data_de_nascimento"
  #      And I press "Selecionar"
  #      And I choose "Masculino"
  #      And I type "Guarulhos" in the field "municipio"
  #      And I press "UF"
  #      And I choose "SP"
  #      When I press "Enviar"
  #      Then I should see "Olá gustavo"

  Scenario: User not registered
	  When I visit site page "/cadastro"
      Then I fill in "first_name" with "gustavo"
	  Then I should see "Welcome to Codeschool!" 
	  And I fill in "Email or username:" with "pedro"
	  And I fill in "Password" with "teste"
	  Then I press "Next"
	  Then I should see "Please enter a correct username or email and password. Note that both fields are case-sensitive"
