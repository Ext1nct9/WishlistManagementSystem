Feature: delete a wishlist
  As a user,
  I want to delete an existing wishlist.
  So that I can manage my wishlist more effectively.

  Background:
    Given the following user accounts exist in the system:
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi1      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |
    And there exists following wishlists:
      | wishlist_id | userAccountId   | name     | description      |
      | 1           | 1               | Dress    | dresses for me   |
      | 2           | 1               | Cars     | dream cars       |
      | 3           | 1               | Books    | favorite novels  |
      | 4           | 2               | Tech     | gadgets and tech |


  @Wishlist
  Scenario Outline: Successfully delete a wishlist 
    When the user <userAccountId> request to delete a valid wishlist <wishlist_id>
    Then the wishlist <wishlist_id> with name <name>, and description <description> shall not exist under <userAccountId> anymore.
    Examples:
      | wishlist_id | userAccountId   | name       | description |
      | 2           | 1               | Cars       | dream cars  |


  @Wishlist
  Scenario Outline: Failed to delete a wishlist by invalid wishlist id
    When the user <userAccountId> request to delete an invalid wishlist <inValidwishlistId>.
    Then the system shall display the following error message <message>
    Examples: 
      | inValidwishlistId | userAccountId   | message                             |
      | 5                 | 1               | The target Wishlist does not exist. |


  @Wishlist
  Scenario Outline: Failed to delete a wishlist by non-owner
    When the non-owner <invalidUserAccountId> attempts to delete the wishlist with ID <validwishlistId>
    Then the system shall display the following error message <message>
    Examples: 
      | validwishlistId   | invalidUserAccountId   | message                                             |
      | 4                 | 1                      | You do not have permission to delete this Wishlist. |