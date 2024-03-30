Feature: Create, update, or delete an item
  As a user,
  I want to be able to create an item in a wishlist,
  So that I can add items to my wishlists.

  Background:
    Given the system contains the following initial user accounts:
      | userAccountId | email             | username      | password        |
      | 1             | hera@gmail.com    | Hera          | Abcdefghi1      |
      | 2             | zeus@gmail.com    | Zeus          | Thaye12345      |
    And the system contains the following initial wishlists:
      | wishlist_id | userAccountId   | name     | description       |
      | 324         | 1               | School   | academic supplies |
      | 735         | 2               | Brunch   | breakfast lunch   |
    And the following item exists in the system:
      | item_ID  | name    | description | link        | status  | rank | wishlist_id |
      | 908      | Pencil  | for writing | staples.com | 1       | 1    | 324         | 
  
  Scenario Outline: Successful item creation with valid information
    Given the user <userAccountId> owns wishlist <validWishlistID> with name <validWishlistName>
    And the user is logged in with email <email> and password <password>
    When the user enters a valid wishlist id <validWishlistID>, a valid item name <validName>, and a description <Description>
    Then the item <validName> with description <Description> shall exist under <validWishlistID>
      Examples:
        | userAccountId | email             | password        | validWishlistID | validWishlistName | validName | Description |
        | 1             | hera@gmail.com    | Abcdefghi1      | 324             | School            | Eraser    | Erasing     |
        | 2             | zeus@gmail.com    | Thaye12345      | 735             | Brunch            | Eggs      | Dozen       |
