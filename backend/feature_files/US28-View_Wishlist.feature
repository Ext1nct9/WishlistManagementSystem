Feature: View a wishlist
  As a user,
  I want to view a wishlist,
  So that I can see the wishlist's information and its items.

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
    And there exists user permissions to view by wishlist id:
      | userAccountId | wishlist_id | permissions |
      | 1             | 4           | 0b00000001  |
      | 2             | 2           | 0b00000001  |
      | 3             | 3           | 0b00000001  |
    And there exists link permissions to view by wishlist id:
      | linkPermissionId | wishlist_id | permissions |
      | 1                | 2           | 0b00000001  |
      | 2                | 4           | 0b00000001  |

  @Wishlist
  Scenario Outline: The user with permission succesfully view the wishlist
    When the user <userId> with permission request to view a wishlist by wishlist id <wishlistId>
    Then the wishlist name <name>, description <description> shall display by wishlist id <wishlistId>
      Examples:
      | userId | wishlistId | name  | description      |
      | 1      | 1          | Dress | dresses for me   |
      | 2      | 4          | Tech  | gadgets and tech |
      | 3      | 3          | Books | favorite novels  |
      | 2      | 2          | Cars  | dream cars       |


  @Wishlist
  Scenario Outline: The link with permission succesfully view the wishlist
    When the link <linkId> with permission request to view a wishlist by wishlist id <wishlistId>
    Then the wishlist name <name>, description <description> shall display by wishlist id <wishlistId>
      Examples:
      | linkId | wishlistId | name  | description      |
      | 1      | 2          | Cars  | dream cars       |
      | 2      | 4          | Tech  | gadgets and tech |


  @Woojin
  Scenario Outline: the user with no permission of the wishlist unsuccessfully view the wishlist information with name and description
    When the user <invalidUserId> requests to view a wishlist <wishlistId>
    Then the system shall display the following error message <message>
      Examples:
      | invalidUserId | wishlistId | message                                          | 
      | 3             | 2          | You do not have permission to view this wishlist |
      | 2             | 1          | You do not have permission to view this wishlist |
      | 223           | 1          | You do not have permission to view this wishlist |


@Wishlist
  Scenario Outline: the link with no permission of the wishlist unsuccessfully view the wishlist information with name and description
    When the not logged-in user with link id <invalidLinkId> requests to view a wishlist <wishlistId>
    Then the system shall display the following error message <message>
      Examples:
      | invalidLinkId | wishlistId | message                                          | 
      | 2             | 2          | You do not have permission to view this wishlist |
      | 23            | 1          | You do not have permission to view this wishlist |


  @Wishlist
  Scenario Outline: the invalid wishlist unsuccessfully retrieve the data from the db
    When the user <userId> requests to view non-existing wishlist id <invalidWishlistId>
    Then the system shall display the following error message <message>
      Examples:
      | userId | invalidWishlistId | message                             | 
      | 1      | 223               | The target Wishlist does not exist. |
      | 2      | 6                 | The target Wishlist does not exist. |
      | 3      | 123               | The target Wishlist does not exist. |

  