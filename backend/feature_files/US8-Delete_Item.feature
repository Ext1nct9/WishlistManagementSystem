Feature: Create, update, or delete an item
  As a user,
  I want to be able to update the information of an existing item,
  So that I can manage the items in my wishlists by inputting new information.

  Background:
    Given there is a Wishlist Management System
    And the following wishlist exists in the system:
      | Wishlist ID | Creator     | Name             | Description         |
      | 1           | 123         | "My Wishlist"    | "A wishlist for me" |

    And the following item exists in the system:
      | Item ID  | Creator     | Name      | Description   |
      | 546      | 123         | "Pencil"  | "For writing" |

   Scenario: Delete valid item in valid wishlist
    Given the user has a wishlist "<1>"
    Given the user has permission to edit "<1>"
    When the user deletes an item "<546>" in "<1>"
    Then the item is removed from the wishlist
    And the id of the item is deleted

  Scenario: Delete invalid item in valid wishlist
    Given the user has a wishlist "<1>"
    Given the user has permission to edit item "<1>"
    When the user deletes an item "<547>" in wishlist "<1>"
    Then there is an error message "<errormsg>"

  Scenario: Delete valid item in invalid wishlist
    Given the user does not have a wishlist "<2>"
    When the user deletes an item "<546>" in "<2>"
    Then there is an error message "<errormsg>"

  Scenario: Delete valid item with invalid permission
    Given the user has a wishlist "<1>"
    Given the user does not have permission to edit "<1>"
    When the user deletes an item "<546>" in "<1>"
    Then there is an error message "<errormsg>"