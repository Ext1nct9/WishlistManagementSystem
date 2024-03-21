Feature: Create, update, or delete an item
  As a user,
  I want to be able to update the information of an existing item,
  So that I can manage the items in my wishlists by inputting new information.

  Background:
    Given there is a Wishlist Management System
    And the following wishlist exists in the system:
      | Wishlist ID | Creator     | Name             | Description   |
      | 1           | 123   | "My Wishlist"    | "A wishlist for me" |

    And the following item exists in the system:
      | Item ID  | Creator     | Name      | Description   |
      | 546      | 123         | "Pencil"  | "For writing" |

  Scenario: Update valid item
    Given the wishlist "<1>" has an item "<546>"
    Given the user has permission to edit "<1>"
    Given the user has permission to edit "<546>"
    When the user updates an attribute of an item "<546>"
    Then the attribute of the item is updated 

  Scenario: Update invalid item
    Given the wishlist does not have an item "<547>"
    When the user updates an item "<547>"
    Then there is an error message "<errormsg>"

  Scenario: Update valid item with invalid permission
    Given the wishlist "<1>" has an item "<546>"
    Given the user does not have permission edit "<1>"
    When the user edits an item "<546>" in "<1>"
    Then there is an error message "<errormsg>"