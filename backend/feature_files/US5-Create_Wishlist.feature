Feature: Create a wishlist
  As a user,
  I want to create a new wishlist
  So that I can organize items within the wishlist.

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
  Scenario Outline: Successfully create a wishlist with all optional features
    When the valid user <ValidAccountId> enters a valid wishlist name <validName>, and a description <Description>
    Then the wishlist <validName> with dsecription <Description> shall exist under <ValidAccountId>
      Examples:
        | ValidAccountId | validName   | Description          |
        | 1              | Travel Gear | adventure essentials |
        | 2              | Home Decor  | modern accents       |
        | 3              | Tech Toys   | latest gadgets       |
  
  
  @Wishlist
  Scenario Outline: Unsuccessful wishlist creation with an existing wishlist name
    When the user <ValidAccountId> enters an invalid wishlist name <invalidName>, and a description <Description>
    Then the wishlist <invalidName> with description <Description> shall not exist under <ValidAccountId> because of an invalid name
    And the system shall display the following error message <message>
    And an wishlist shall not be created due to the exsiting name
      Examples:
        | ValidAccountId | invalidName | Description         | message                                      |
        | 1              | Cars        | super cars          | Wishlist name already exist in this account. |
        | 2              | Tech        | apple devices       | Wishlist name already exist in this account. |
        | 1              | Dress       | beautiful dresses   | Wishlist name already exist in this account. |
  

  @Wishlist
  Scenario Outline: Unsuccessful wishlist creation without a name
    When the user <ValidAccountId> enters an empty wishlist name, and a description <Description>
    Then the wishlist with description <Description> shall not exist under <ValidAccountId> because of an empty wishlist name
    And the system shall display the following error message <message>
    And an wishlist shall not be created due to the empty name
      Examples:
        | ValidAccountId | name  | Description         | message                        |
        | 1              |       | tech gadgets        | Wishlist name cannot be blank. |
        | 2              |       | cooking utensils    | Wishlist name cannot be blank. |
        | 3              |       | fitness gear        | Wishlist name cannot be blank. |
  

  @Wishlist
  Scenario Outline: Unsuccessful wishlist creation with invalid account id
    When the user <inValidAccountId> enters a valid wishlist name <validName>, and a description <Description>
    Then the wishlist <validName> with description <Description> shall not exist becuase of <inValidAccountId> user
    And the system shall display the following error message <message>
    And a wishlist shall not be created due to invalid user id
      Examples:
        | inValidAccountId | validName    | Description           | message                            |
        | 4                | Travel Gearn | adventure essentials  | The user_account_id does not exist.|
        | 52               | Home Decor   | modern accents        | The user_account_id does not exist.|
        | 231              | Tech Toys    | latest gadgets        | The user_account_id does not exist.|
