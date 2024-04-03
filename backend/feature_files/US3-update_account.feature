Feature: Update an account
    As a user,
    I want to update my existing account information,
    So that I can manage my account information for the What2Buy system.

  Background: 
    Given there exist the following user accounts:
      | userAccountId | email             | username      | password        |
      |             1 | whamuzi@gmail.com | MrReborn      | Abcdefghi!      |
      |             2 | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      |             3 | willy@gmail.com   | tortue_perdue | jaimelest0rtues |

  Scenario Outline: Update an email successfully
    Given the user with email <oldEmail>, <password> is logged into their account
    When the user attempts to update their account <userAccountId> with valid input email <newEmail>
    Then the old account with information with email <oldEmail>, username <username> and password <password> for account <userAccountId> shall no longer exist
    And the new account with information with email <newEmail>, username <username> and password <password> for account <userAccountId> shall exist

    Examples: 
      | userAccountId | oldEmail          | newEmail          | username | password   |
      |             1 | whamuzi@gmail.com | r.z.d.r@gmail.com | MrReborn | Abcdefghi1 |

  Scenario Outline: Update a username successfully
    Given the user with <email>, <password> is logged into their account
    When the user attempts to update their account <userAccountId> with valid input username <newUsername>
    Then the old account information with email <email>, username <oldUsername> and password <password> for account <userAccountId> shall no longer exist
    And the new account information with email <email>, username <newUsername> and password <password> for account <userAccountId> shall exist

    Examples: 
      | userAccountId | email           | oldUsername   | newUsername | password        |
      |             3 | willy@gmail.com | tortue_perdue | fidelstick  | jaimelest0rtues |

  Scenario Outline: Update a password successfully
    Given the user <email>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with valid input password <newPassword>
    Then the old information with email <email>, username <username> and password <oldPassword> for account <userAccountId> shall no longer exist
    And the new information with email <email>, username <username> and password <newPassword> for account <userAccountId> shall exist

    Examples: 
      | userAccountId | email             | username | oldPassword  | newPassword |
      |             2 | mawpiew@gmail.com | Lost Boy | VixxenBibi#1 | VixxenBibi1 |

  Scenario Outline: Update an account unsuccessfully by not setting a new email
    Given the user <oldEmail>, <password> is logged into their account
    When the user attempts to update their account <userAccountId> with an empty email
    Then the old account with information with email <oldEmail>, username <username> and password <password> for account <userAccountId> shall still exist
    And the system shall show the following error <error>

    Examples: 
      | userAccountId | oldEmail          | newEmail | username | password   | error                                         |
      |             1 | whamuzi@gmail.com |          | MrReborn | Abcdefghi1 | Email entry must not be empty (no whitespace) |

  Scenario Outline: Update an account unsuccessfully by not setting a username
    Given the user <email>, <password> is logged into their account
    When the user attempts to update their account <userAccountId> with an empty username
    Then the old account information with email <email>, username <oldUsername> and password <password> for account <userAccountId> shall still exist
    And the system shall show the following error <error>

    Examples: 
      | userAccountId | email           | oldUsername   | newUsername | password        | error                                            |
      |             3 | willy@gmail.com | tortue_perdue |             | jaimelest0rtues | Username entry must not be empty (no whitespace) |

  Scenario Outline: Update an account unsuccessfully by not setting a password
    Given the user <email>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with an empty password
    Then the old information with email <email>, username <username> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>

    Examples: 
      | userAccountId | email             | username | oldPassword  | newPassword | error                                            |
      |             2 | mawpiew@gmail.com | Lost Boy | VixxenBibi#1 |             | Password entry must not be empty (no whitespace) |

  Scenario Outline: Update an account unsuccessfully by not following the password's restrictions
    Given the user <email>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with invalid input password <newPassword>
    Then the new information with <email>, username <username> and password <newPassword> for account <userAccountId> shall not exist
    And the old information with email <email>, username <username> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>

    Examples: 
      | userAccountId | email             | username | oldPassword  | newPassword | error                                                              |
      |             2 | mawpiew@gmail.com | Lost Boy | VixxenBibi#1 | VixxenBibi! | Password entry must contain at least one number                    |
      |             2 | mawpiew@gmail.com | Lost Boy | VixxenBibi#1 | V i x x e n | Password entry must be at least 10 characters (no whitespace) long |
