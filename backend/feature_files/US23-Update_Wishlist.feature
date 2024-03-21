Feature: Update a wishlist
  As a user,
  I want to update the information of an existing wishlist.
  So that I can manage the wishlists more effectively.

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
    And there exists user permissions:
      | userAccountId | wishlist_id | permissions |
      | 1             | 4           | 0b00000010  |
      | 2             | 2           | 2           |
      | 3             | 3           | 0b00000010  |
    And there exists link permissions:
      | linkPermissionId | wishlist_id | permissions |
      | 1                | 2           | 2           |
      | 2                | 4           | 0b00000010  |

  @Wishlist
  Scenario Outline: the user with permission of the wishlist sccessfully update the wishlist information with name and description
    When the valid user <validAccountId> request to update a wishlist <validWishlistId> with name <validName>, and description <validDescription>
    Then the <validWishlistId> with the <oldName> and <oldDescription> shall no longer exist
    Then the <validWishlistId> with the <validName> and <validDescription> shall exist      
      Examples:
        | validAccountId | validWishlistId | validName        | validDescription     | oldName     | oldDescription   |
        | 1              | 1               | Travel Gear      | adventure essentials | Dress       | dresses for me   |
        | 2              | 4               | Home Decor       | modern accents       | Tech        | gadgets and tech |
        | 2              | 2               | Super Cars       | my favorite cars     | Cars        | dream cars       |
        | 3              | 3               | Home Renovation  | modern home upgrades | Books       | favorite novels  | 

  @Wishlist
  Scenario Outline: the user with link permission of the wishlist sccessfully update the wishlist information with name and description
    When the valid link <validLinkId> request to update a wishlist <validWishlistId> with name <validName>, and description <validDescription>
    Then the <validWishlistId> with the <oldName> and <oldDescription> shall no longer exist
    Then the <validWishlistId> with the <validName> and <validDescription> shall exist      
      Examples:
        | validLinkId    | validWishlistId | validName        | validDescription          | oldName     | oldDescription   |
        | 1              | 2               | Adventure Gear   | outdoor exploration gear  | Cars        | dream cars       |
        | 2              | 4               | Home Decor       | modern accents            | Tech        | gadgets and tech |
    
  @Wishlist
  Scenario Outline: the user with no permission of the wishlist unsuccessfully update the wishlist information with name and description
    When the invalid user <invalidAccountId> request to update a wishlist <validWishlistId> with name <validName>, and description <validDescription>
    Then the <validWishlistId> with the <validName> and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | invalidAccountId  | validWishlistId | validName        | validDescription          | message                                          |
        | 2                 | 3               | Adventure Gear   | outdoor exploration gear  | You do not have permission to edit this wishlist |
        | 3                 | 1               | Home Decor       | modern accents            | You do not have permission to edit this wishlist |
    

  @Wishlist
  Scenario Outline: the link with no permission of the wishlist unsuccessfully update the wishlist information with name and description
    When the invalid link <inValidLinkId> request to update a wishlist <validWishlistId> with name <validName>, and description <validDescription>
    Then the <validWishlistId> with the <validName> and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | inValidLinkId  | validWishlistId | validName           | validDescription              | message                                          |
        | 3              | 3               | Travel Essentials   | essentials for your journey   | You do not have permission to edit this wishlist |
        | 4              | 1               | Fitness Gear        | gear for a healthy lifestyle  | You do not have permission to edit this wishlist |
    
    
  @Wishlist
  Scenario Outline: the user with non existing wishlist unsuccessfully update the wishlist information with name and description
    When the user <validAccountId> request to update a wishlist <inValidWishlistId> with name <validName>, and description <validDescription>
    Then the <inValidWishlistId> with the <validName> and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | validAccountId  | inValidWishlistId | validName           | validDescription              | message                             |
        | 1               | 95                | Travel Essentials   | essentials for your journey   | The target Wishlist does not exist. |
        | 2               | 249               | Fitness Gear        | gear for a healthy lifestyle  | The target Wishlist does not exist. |


  @Wishlist
  Scenario Outline: the user with valid wishlist unsuccessfully update the wishlist information with an empty name and description
    When the user <validAccountId> request to update a wishlist <validWishlistId> with an empty name, and description <validDescription>
    Then the <validWishlistId> with an empty name and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | validAccountId  | validWishlistId | inValidName   | validDescription          | message                        |
        | 1               | 3               |               | Harry potter series       | Wishlist name cannot be blank. |
        | 1               | 4               |               | PC accessories            | Wishlist name cannot be blank. |
  

  @Wishlist
  Scenario Outline: the user with valid wishlist unsuccessfully update the wishlist information with an existing name and description
    When the user <validAccountId> request to update a wishlist <validWishlistId> with an existing name <inValidName>, and description <validDescription>
    Then the <validWishlistId> with an existing name <inValidName> and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | validAccountId  | validWishlistId | inValidName   | validDescription          | message                                      |
        | 1               | 3               | Books         | Harry potter series       | Wishlist name already exist in this account. |
        | 1               | 4               | Tech          | PC accessories            | Wishlist name already exist in this account. |
  

  @Wishlist
  Scenario Outline: the invalid user, and invalid link with valid wishlist unsuccessfully update the wishlist information with a valid name and description
    When the user <inValidAccountId>, with the link <inValidLinkId> requests to update a wishlist <validWishlistId> with name <validName>, and description <validDescription>
    Then the <validWishlistId> with the <validName> and <validDescription> shall not exist
    And the system shall display the following error message <message>
      Examples:
        | inValidAccountId  | inValidLinkId  | validWishlistId | validName           | validDescription              | message                                          |
        | 134               | 23             | 3               | Pet Supplies        | items for your furry friends  | You do not have permission to edit this wishlist |
        | 102               | 142            | 4               | Gardening Tools     | tools for a beautiful garden  | You do not have permission to edit this wishlist |
