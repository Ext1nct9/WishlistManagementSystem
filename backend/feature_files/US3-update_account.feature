Feature: Update an account
    As a user,
    I want to update my existing account information,
    So that I can manage my account information for the What2Buy system.

Background:
    Given there exist the following user accounts: 
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi!      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |

@Estefania
Scenario Outline: Update an account successfully
    Given the user <oldEmail>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with valid inputs email <newEmail>, username <newUsername> and password <newPassword>
    Then the old information with email <oldEmail>, username <oldUsername> and password <oldPassword> for account <userAccountId> shall no longer exist
    And the new information with email <newEmail>, username <newUsername> and password <newPassword> for account <userAccountId> shall exist
    
    Examples:
      | userAccountId | oldEmail          | newEmail          | oldUsername   | newUsername | oldPassword     | newPassword  |
      | 1             | whamuzi@gmail.com | r.z.d.r@gmail.com | MrReborn      | MrReborn19  | Abcdefghi1      | ABCDEFGHi1   | 
      | 2             | mawpiew@gmail.com | mawpiew@gmail.com | Lost Boy      | Lost Boy    | VixxenBibi#1    | VixxenBibi1  | 
      | 3             | willy@gmail.com   | willy@gmail.com   | tortue_perdue | fidelstick  | jaimelest0rtues | newPassw0rd  | 

@Estefania
  Scenario Outline: Update an account unsuccessfully by not following the entries' restrictions
    Given the user <oldEmail>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with invalid inputs email <newEmail>, username <newUsername> and password <newPassword>
    Then the new information with <newEmail>, username <newUsername> and password <newPassword> for account <userAccountId> shall not exist
    And the old information with email <oldEmail>, username <oldUsername> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>
    
    Examples:
      | userAccountId | oldEmail          | newEmail          | oldUsername   | newUsername | oldPassword     | newPassword  | error                                                              |
      | 2             | mawpiew@gmail.com | mawpiew@gmail.com | Lost Boy      | Lost Boy    | VixxenBibi#1    | VixxenBibi!  | Password entry must contain at least one number                    |
      | 2             | mawpiew@gmail.com | mawpiew@gmail.com | Lost Boy      | Lost Boy    | VixxenBibi#1    | V i x x e n  | Password entry must be at least 10 characters (no whitespace) long |

@Estefania
  Scenario Outline: Update an account unsuccessfully by not setting a new email
    Given the user <oldEmail>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with username <newUsername> and password <newPassword>
    Then the old information with email <oldEmail>, username <oldUsername> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>
    
    Examples:
      | userAccountId | oldEmail          | newEmail          | oldUsername   | newUsername | oldPassword     | newPassword  | error                                         |
      | 1             | whamuzi@gmail.com |                   | MrReborn      | MrReborn19  | Abcdefghi1      | ABCDEFGHi1   | Email entry must not be empty (no whitespace) |

@Estefania
  Scenario Outline: Update an account unsuccessfully by not setting a password
    Given the user <oldEmail>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with email <newEmail> and username <newUsername>
    Then the old information with email <oldEmail>, username <oldUsername> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>
    
    Examples:
      | userAccountId | oldEmail          | newEmail          | oldUsername   | newUsername | oldPassword     | newPassword  | error                                            |
      | 2             | mawpiew@gmail.com | mawpiew@gmail.com | Lost Boy      | Lost Boy    | VixxenBibi#1    |              | Password entry must not be empty (no whitespace) |

@Estefania
  Scenario Outline: Update an account unsuccessfully by not setting a username
    Given the user <oldEmail>, <oldPassword> is logged into their account
    When the user attempts to update their account <userAccountId> with email <newEmail> and password <newPassword>
    Then the old information with email <oldEmail>, username <oldUsername> and password <oldPassword> for account <userAccountId> shall still exist
    And the system shall show the following error <error>
    
    Examples:
      | userAccountId | oldEmail          | newEmail          | oldUsername   | newUsername | oldPassword     | newPassword  | error                                            |
      | 3             | willy@gmail.com   | willy@gmail.com   | tortue_perdue |             | jaimelest0rtues | newPassw0rd  | Username entry must not be empty (no whitespace) |

