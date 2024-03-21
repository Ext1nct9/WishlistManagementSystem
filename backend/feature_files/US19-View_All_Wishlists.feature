Feature: View all wishlists
  As a user,
  I want to view all my existing wishlists.
  So that I can view the wishlists in my account.
  
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
  Scenario Outline: Successfully view all the wishlists with user account
    When the user <userAccountId> requests to view all the wishlists
    Then all the wishlists in the database for user <userAccountId> match the query result      
      Examples:
        | userAccountId | 
        | 1             |
        | 2             |


  @Wishlist
  Scenario Outline: Unsuccessfully view all the wishlists with invalid user account
    When the user <userAccountId> with invalid account id requests to view all wishlists
    Then the system shall display the following error message <message>
      Examples:
        | userAccountId | message                          |
        | 123           | The target user does not exist.  |
        | 4             | The target user does not exist.  | 


  @Wishlist
  Scenario Outline: Unsuccessfully view all the wishlists with user account who don't have wishlists
    When the user <userAccountId> with account id requests to view wishlists
    Then the system shall display the following error message <message>
      Examples:
        | userAccountId | message                              |
        | 3             | The user does not have any wishlist  |
