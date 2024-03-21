Feature: Login
    As a user,
    I want to be able to login to my account,
    So that I can manage my account information for the What2Buy system and access the systems' features.

Background:
    Given there exist the following user accounts:
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi1      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |

@William
Scenario Outline: Logging in successfully
    Given the user is on the login page
    When the user enters their email <email>
    And the user enters the password <password>
    Then the user shall log in successfully
    Examples:
      | email             | password        |
      | whamuzi@gmail.com | Abcdefghi1      |
      | mawpiew@gmail.com | VixxenBibi#1    |
      | willy@gmail.com   | jaimelest0rtues |


  @William
  Scenario Outline: Logging in unsuccessfully due to invalid password or invalid email
    Given the user is on the login page

    When the user enters their email <email>
    And the user enters the password <invalidPassword>
    Then the user shall not log in successfully 
    And the system shall show the following error message <message>

    Examples:
      | email             | invalidPassword | message                          |
      | whamuzi@gmail.com | Zyxwsdadw2      | Unauthorized: Incorrect password |
      | mawpiew@gmail.com | vIxxenBib       | Unauthorized: Incorrect password |
      | willy77@gmail.com | jaimelest0rtues | Unauthorized: User not found     |