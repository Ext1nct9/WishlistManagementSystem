Feature: Create, update, or delete an item
  As a user,
  I want to be able to create an item in a wishlist,
  So that I can add items to my wishlists.

  Background:
    Given there is a Wishlist Management System
    And the following wishlist exists in the system:
      | Wishlist ID | Creator     | Name             | Description         |
      | 1           | 123         | "My Wishlist"    | "A wishlist for me" |

    And the following item exists in the system:
      | Item ID  | Creator     | Name      | Description   |
      | 546      | 123         | "Pencil"  | "For writing" |
      
  Scenario: Create valid item in valid wishlist
    Given the user has a wishlist "<1>"
    Given the user has permission to edit "<1>"
    When the user creates an item "<item>" in "<1>"
    Then a unique item id is given to the item
    And the item is added to the wishlist "<1>"

  Scenario: Create item with empty name attribute
    Given the user has a wishlist "<1>"
    Given the user has permission to edit "<1>"
    When the user creates an item "<item>" with empty name attribute
    Then there is an error message "<errormsg>"
