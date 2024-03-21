Feature: Add a comment
As a user, 
I want to be able to create a comment on an item 
So that I can leave a message to the users of the wishlist.

  Background:
    Given the wishlist 123 has an item 546

  Scenario: Create a comment on an item
    Given the user has permission to comment 546
    When the user writes a comment in 546
    Then the comment is recorded in the system
    And the comment is automatically assigned a username and ID

  Scenario: Create a comment on a restricted item
    Given the user does not have permission to comment 123
    When the user writes a comment in 546
    Then the comment is not recorded in the system
    And there is an error message You do not have permission to comment on this item

  Scenario: Create an empty comment on an item
    Given the user has permission to comment 123
    When the user writes an empty comment in 546
    Then the comment is not recorded in the system
    And there is an error message body cannot be blank
