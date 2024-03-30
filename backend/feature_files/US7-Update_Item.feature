Feature: Create, update, or delete an item
  As a user,
  I want to be able to update the information of an existing item,
  So that I can manage the items in my wishlists by inputting new information.

  Background:
    Given the system contains the following user accounts:
      | userAccountId | email             | username      | password        |
      | 1             | tonyand@gmail.com | TonyAnde      | Abcdefghi1      |
      | 2             | geminit@gmail.com | GeminiTa      | Thaye12345      |
    And the system contains the following wishlists:
      | wishlist_id | userAccountId   | name     | description       |
      | 1           | 1               | School   | academic supplies |
      | 2           | 2               | Brunch   | breakfast lunch   |
    And the following items exist in the system:
      | item_ID  | name    | description | link        | status  | rank | wishlist_id |
      | 123      | Pencil  | for writing | staples.com | 1       | 1    | 1           |
      | 456      | Bacon   | for cooking | maxi.ca     | 1       | 1    | 2           |
    And the system contains the following user permissions:
      | userAccountId | wishlist_id | permissions |
      | 1             | 1           | 0b00000010  |
      | 2             | 2           | 0b00000010  |

@Item
  Scenario Outline: the user with permission of the wishlist successfully updates the item information with name and description
    When the valid user <validAccountId> request to update an item <validItemId> with name <validName>, description <new_desc>, and status <status>
    And the user <validAccountId> has permission <validPermission> to update wishlist < validWishlistId >
    Then the item <validItemId> with the <oldName>, <oldDescription> shall no longer exist
    Then the item <validItemId> with the <validName> and <new_desc> shall exist in the wishlist <validWishlistId>
      Examples:
        | validAccountId | validPermission | validWishlistId | validItemId | validName    | new_desc     | status | oldName | oldDescription |
        | 1              | 0b00000010      | 1               | 123         | Fountain Pen | good writing | 1      | Pencil  | for writing    |
        | 2              | 0b00000010      | 2               | 456         | Tofu         | vegan recipe | 1      | Bacon   | for cooking    |