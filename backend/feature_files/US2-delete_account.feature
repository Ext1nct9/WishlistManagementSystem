Feature: Delete an account
    As a user,
    I want to delete my existing account information,
    So that I can delete my account information for the What2Buy system.


Scenario Outline: Delete an account successfully
    Given there exist the following user accounts: 
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi1      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |
    And the user <email>, <password> is logged into their account
    When the user attempts to delete their account <userAccountId>
    Then the user <userAccountId> shall no longer exist
    And the total number of accounts shall be <numAccounts>
    
    Examples: 
      | userAccountId | email             | password        | numAccounts |
      | 1             | whamuzi@gmail.com | Abcdefghi1      | 2           |
      | 2             | mawpiew@gmail.com | VixxenBibi#1    | 2           |
      | 3             | willy@gmail.com   | jaimelest0rtues | 2           |