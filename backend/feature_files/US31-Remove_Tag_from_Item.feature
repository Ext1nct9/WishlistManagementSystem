Feature: Remove a tag from item
As a user,
I want to be able to remove an existing tag from an existing item
So that I can reclassify the items in my wishlist.


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
    And there exist the following itemTags in the wishlist:
        | itemTag  |
        | (1,1)    |
        | (1,3)    |
        | (2,2)    |


Scenario Outline: Remove a tag from an existing item successfully
    Given the user <email>, <password> has the permission to assign tags to items
    When the user removes the itemTag <item>, <tagToRemove> in wishlist <wishlist>
    Then the itemTag <item>, <tagToRemove> shall no longer exist

    Examples: 
        | email             | password     | wishlist | item | tagToRemove |
        | mawpiew@gmail.com | VixxenBibi#1 | 1        | 1    | 3           |
        | mawpiew@gmail.com | VixxenBibi#1 | 1        | 2    | 2           |


Scenario Outline: Remove a tag from an existing item unsuccessfully
    Given the user <email>, <password> does not have the permission to assign tags to items
    When the user attempts to remove itemTag <item>, <tagToRemove> in wishlist <wishlist>
    Then the itemTag <item>, <tagToRemove> shall still exist
    And the system shall raise the error <error>
    
    Examples: 
        | email             | password   | wishlist | item | tagToRemove | error                                       |
        | whamuzi@gmail.com | Abcdefghi1 | 1        | 1    | 3           | Not authorized to remove a tag from an item |
        | whamuzi@gmail.com | Abcdefghi1 | 1        | 2    | 2           | Not authorized to remove a tag from an item |