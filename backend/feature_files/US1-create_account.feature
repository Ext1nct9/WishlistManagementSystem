Feature: Create an account
    As a user,
    I want to create an account,
    So that I can log into and manage my account for the What2Buy system.

Background:
    Given there exist the following user accounts: 
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi1      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |

  @William
  Scenario Outline: Successful account creation with valid information
    When the user enters a valid email <validEmail>, a username <Username> and a secure password <validPassword>
    Then the account <validEmail> with username <Username> and password <validPassword> shall exist
      Examples:
        | validEmail        | Username    | validPassword   |
        | willy11@gmail.com | willy11     | Abcdefgh11      |
        | mawpie@gmail.com  | mawpie      | VixxenBibi1     |
        | animal@gmail.com  | animal      | Jaimelest0rtues |
        | willy12@gmail.com | willy12     | Abcdefgh11      |
        | mawp1e@gmail.com  | mawp1e      | VixxenBibi1     |
        | an1mal@gmail.com  | an1mal      | Jaimelest0rtues |

  @William
  Scenario Outline: Unsuccessful account creation with an existing email
    When the user enters an invalid email <invalidEmail>, a username <Username> and a secure password <validPassword>
    Then the account <invalidEmail> with username <Username> and password <validPassword> shall not exist because of an invalid email
    And the system shall show the following error message <message>
    And an account shall not be created due to the email
      Examples:
        | invalidEmail      | Username | validPassword   | message              |
        | mawpiew@gmail.com | mawpie   | VixxenBibi1     | Email already in use |
        | willy@gmail.com   | willy11  | Jaimelest0rtues | Email already in use |

  @William
  Scenario Outline: Unsuccessful account creation with a weak password
    When the user enters a valid email <validEmail>, a username <Username> and an insecure password <invalidPassword>
    Then the account <validEmail> with username <Username> and password <invalidPassword> shall not exist because of an invalid password
    And the system shall show the following error message <message>
    And an account shall not be created due to the password
      Examples:
        | validEmail        | Username    | invalidPassword | message                                                                      |
        | willy11@gmail.com | willy11     | Abcd1           | Password must be at least 10 characters long and contain at least one number |
        | mawpie@gmail.com  | mawpie      | VixxenBibi      | Password must be at least 10 characters long and contain at least one number |
        | mawpie@gmail.com  | mawpie      | Alex lai        | Password entry must not contain whitespace                                   |

          
          
  @William
  Scenario Outline: Unsuccessful account creation with missing password
    When the user enters a valid email <validEmail>, a username <Username> and no password
    Then the account <validEmail> with username <Username> shall not exist because of a missing password field
    And the system shall show the following error message <message>
    And an account shall not be created due to the password
      Examples:
        | validEmail        | Username    | password | message                                                                      |
        | mawpie@gmail.com  | mawpie      |          | Missing required fields                                                      |
  

  @William
  Scenario Outline: Unsuccessful account creation with missing email
    When the user enters no email, a username <Username> and a password <password>
    Then the account <Username> with password <password> shall not exist because of a missing email field
    And the system shall show the following error message <message>
    And an account shall not be created due to the password
      Examples:
        | validEmail        | Username    | password    | message                                                                      |
        |                   | mawpie      | VixxenBibi1 | Missing required fields                                                      |
      

  @William
  Scenario Outline: Unsuccessful account creation with missing username
    When the user enters a valid email <validEmail>, no username and a password <password>
    Then the account <validEmail> with password <password> shall not exist because of a missing username field
    And the system shall show the following error message <message>
    And an account shall not be created due to the password
      Examples:
        | validEmail        | Username    | password     | message                                                                      |
        | mawpie@gmail.com  |             | VixxenBibi1  | Missing required fields                                                      |