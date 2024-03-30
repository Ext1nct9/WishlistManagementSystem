Feature: Create, update, or delete an item
  As a user,
  I want to be able to update the information of an existing item,
  So that I can manage the items in my wishlists by inputting new information.

  Background:
    Given the system has the following user account:
      | userAccountId | email             | username      | password        |
      | 1             | tonyand@gmail.com | TonyAnde      | Abcdefghi1      |
    And the system has the following wishlist:
      | wishlist_id | userAccountId   | name     | description       |
      | 1           | 1               | School   | academic supplies |
    And the system has the following items:
      | item_ID  | name    | description | link        | status  | rank | wishlist_id |
      | 123      | Pencil  | for writing | staples.com | 1       | 1    | 1           |
      | 456      | Eraser  | for erasing | staples.com | 1       | 1    | 1           |
    And the system has the following user permission:
      | userAccountId | wishlist_id | permissions |
      | 1             | 1           | 0b00000111  |
      | 2             | 1           | 0b00000000  |

   @Item
    Scenario Outline: the user with permission of the wishlist successfully deletes an item
    When the valid user <validAccountId> requests to delete an item <validItemId>
    And the user <validAccountId> has permission <validPermission> to edit items <validWishlistId>
    Then the item <validItemId> with the <name>, <description> shall no longer exist in the system
      Examples:
        | validAccountId | validPermission | validWishlistId | validItemId | name    | description |
        | 1              | 0b00000111      | 1               | 123         | Pencil  | for writing |
        | 1              | 0b00000111      | 1               | 456         | Eraser  | for erasing |