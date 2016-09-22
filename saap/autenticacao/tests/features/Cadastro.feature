Feature: Cadastro de Usuário
  To get acess to the saap features
  As an citizen 
  I want to register my self

Scenario: login valido
        When I visit site page "/cadastro"
        Then I fill in "first_name" with "user_first"
        Then I fill in "last_name" with "user_last"
        Then I fill in "username" with "user_username"
        Then I fill in "email" with "user_email@email.com"
        Then I fill in "confirmacao_email" with "user_email@email.com"
        Then I fill in "password" with "user_password"
        Then I fill in "confirmacao_password" with "user_password"
        Then I fill in "data_de_nascimento" with "1990-10-10"
    	Then I select "Masculino" from "Selecionar"
        #	Then I should see "Welcome to Codeschool!" 
        #	Then I click "SIGN UP"
        #	And I fill in "id_first_name" with "Teste"
        #	And I fill in "id_last_name" with "Junior"
        #	And I fill in "id_username" with "teste"
        #	And I fill in "id_email" with "fjalkdjflaksdjal"
        #	And I fill in "id_password1" with "testando"
        #	And I fill in "id_password2" with "testando"
        #	Then I press "Next"
        #	Then I should see "Enter a valid email address."
        #
        #Scenario: Duplicate username
        #	Given System create user "jteste2" with password "teste"
        #	When I visit site page "/accounts/login"
        #	Then I should see "Welcome to Codeschool!" 
        #	Then I click "SIGN UP"
        #	And I fill in "id_first_name" with "Teste"
        #	And I fill in "id_last_name" with "Junior"
        #	And I fill in "id_username" with "jteste2"
        #	And I fill in "id_email" with "teste2@teste.com"
        #	And I fill in "id_password1" with "testando"
        #	And I fill in "id_password2" with "testando"
        #	Then I press "Next"
        #	Then I should see "This username is already taken."
        #
        #Scenario: Valide fields
        #	When I visit site page "/accounts/login"
        #	Then I should see "Welcome to Codeschool!" 
        #	Then I click "SIGN UP"
        #	And I fill in "id_first_name" with "Teste"
        #	And I fill in "id_last_name" with "Junior"
        #	And I fill in "id_username" with "teste"
        #	And I fill in "id_email" with "teste@testando.com"
        #	And I fill in "id_password1" with "testando"
        #	And I fill in "id_password2" with "testando"
        #	And I fill in "id_date_of_birth" with "10/07/1992"
        #	And I select "male" from "Gender" 
        #	And I fill in "id_about_me" with "I am a test user for checking if the register form is working well"
        #	Then I press "Next"
        #	Then The browser's URL should contain "teste"




        #  Scenario: User not registered
        #	  When I visit site page "/cadastro"
        #          Then I fill in "first_name" with "gustavo"
        #	  Then I should see "Welcome to Codeschool!" 
        #	  And I fill in "Email or username:" with "pedro"
        #	  And I fill in "Password" with "teste"
        #	  Then I press "Next"
        #	  Then I should see "Please enter a correct username or email and password. Note that both fields are case-sensitive"
