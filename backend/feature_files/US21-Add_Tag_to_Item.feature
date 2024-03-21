Feature: Add a tag to item
As a user,
I want to be able to add an existing tag to an existing item
So that I can classify the items in my wishlist.


Background: 
    Given there exist the following accounts: 
        | userAccountId | email             | username | password     |
        | 1             | whamuzi@gmail.com | MrReborn | Abcdefghi1   |
        | 2             | mawpiew@gmail.com | Lost Boy | VixxenBibi#1 |
    And there is a wishlist:
        | wishlist | name          | description     | user_account_id |
        | 1        | Trip to Italy | Graduation gift | 2               |
    And there exist the following tags in the wishlist:
        | tag | label      | color | wishlist |
        | 1   | clothes    | blue  | 1        |
        | 2   | essentials | pink  | 1        |
        | 3   | medical    | red   | 1        |
     And there exist the following items in the wishlist:
        | item | name         | description       | link           | status  | rank | wishlist |
        | 1    | bathing suit | to swim           | decathlon.com  | pending | 1    | 1        |
        | 2    | sunscreen    | to protect myself | pharmaprix.com | pending | 2    | 1        |
    And there exist the following items with the following tags in the wishlist:
        | itemTag  |
        | (1,1)    |


Scenario Outline: Add a tag to an existing item successfully
    Given the user <email>, <password> has the permission to assign tags to items
    When the user adds a tag <tagToAdd> to the item <item> in wishlist <wishlist>
    Then the itemTag <item>, <tagToAdd> shall exist

    Examples: 
        | email             | password     | wishlist | item | tagToAdd |
        | mawpiew@gmail.com | VixxenBibi#1 | 1        | 1    | 3        |
        | mawpiew@gmail.com | VixxenBibi#1 | 1        | 2    | 2        |


Scenario Outline: Add a tag to an existing item unsuccessfully
    Given the user <email>, <password> does not have the permission to assign tags to items
    When the user attempts to add a tag <tagToAdd> to the item <item> in wishlist <wishlist>
    Then the itemTag <item>, <tagToAdd> shall not exist
    And the system shall raise the error <error>

    Examples: 
        | email             | password   | wishlist | item | tagToAdd | error                               |
        | whamuzi@gmail.com | Abcdefghi1 | 1        | 1    | 3        | Not authorized to add tags to items |
        | whamuzi@gmail.com | Abcdefghi1 | 1        | 2    | 2        | Not authorized to add tags to items |