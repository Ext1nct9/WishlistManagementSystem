Feature: Create a tag under wishlist
  As a user,
  I want to be able to create a tag in a wishlist,
  So that I can categorize the items in my wishlist.

Background: 
  Given the following user accounts exist in the system:
      | userAccountId | email             | username      | password        |
      | 1             | whamuzi@gmail.com | MrReborn      | Abcdefghi1      |
      | 2             | mawpiew@gmail.com | Lost Boy      | VixxenBibi#1    |
      | 3             | willy@gmail.com   | tortue_perdue | jaimelest0rtues |
  And the following wishlists exist in the system:
      | wishlist_id | userAccountId   | name     | description      |
      | 1           | 1               | Dress    | dresses for me   |
      | 2           | 2               | Cars     | dream cars       |
      | 3           | 3               | Books    | favorite novels  |
      | 4           | 3               | Tech     | gadgets and tech |
  And the following tags exist in the system:
    | TagID  | WishlistID  | Label   | Color  |
    | 1      | 1           | Toys    | Purple |
    | 2      | 2           | Books   | Blue   |
    | 3      | 3           | Music   | Green  |
    | 4      | 4           | Food    | Red    |
  And the following user permissions exist in the system:
      | userAccountId | wishlist_id | permissions |
      | 1             | 2           | 0b00001001  |
      | 2             | 1           | 3           |
      | 3             | 2           | 0b00100011  |
      | 3             | 1           | 0b00001011  |
  And the following link permissions exist in the system:
      | linkPermissionId | wishlist_id | permissions |
      | 1                | 1           | 0b00001011  |
      | 2                | 2           | 0b00000101  |
      | 3                | 3           | 0b00001001  |
      | 4                | 4           | 0b00010001  |

  @Tag
Scenario Outline: User creates a tag under a wishlist with label and color
  When the valid user <ValidAccountId> in wishlist <WishlistID> enters a valid label <Label>, and a color <Color> for the tag
  Then a tag with an automatically assigned ID, label <Label>, and color <Color> shall be created under the wishlist <WishlistID>
    Examples:
      | ValidAccountId | WishlistID | Label   | Color  |
      | 1              | 1          | Food    | Red    |
      | 1              | 1          | Games   | Green  |
      | 2              | 2          | Games   | Green  |
      | 2              | 2          | Music   | Yellow |
      | 1              | 2          | Cat     | Black  |
      | 3              | 1          | Dog     | White  |
  
  @Tag
Scenario Outline: User creates a tag under a wishlist without providing color
  When the valid user <ValidAccountId> in wishlist <WishlistID> enters a valid label <Label>, and does not provide a color for the tag
  Then a tag with an automatically assigned ID, label <Label>, and a random color shall be created under the wishlist <WishlistID>
    Examples:
      | ValidAccountId | WishlistID | Label   |
      | 1              | 1          | Food    |
      | 1              | 1          | Games   |
      | 2              | 2          | Games   |
      | 2              | 2          | Music   |
 
  @Tag
Scenario Outline: User tries to create a tag without providing a label
  When the valid user <ValidAccountId> in wishlist <WishlistID> does not provide a label for the tag
  Then a tag shall not be created under the wishlist <WishlistID>
  And the system shall show the following error message <message>
    Examples:
      | ValidAccountId | WishlistID | message                                   |
      | 1              | 1          | Tag label cannot be blank.                |
      | 2              | 2          | Tag label cannot be blank.                |
 
  @Tag
Scenario Outline: User tries to create a tag with a label that already exists in the wishlist
  When the valid user <ValidAccountId> in wishlist <WishlistID> enters a label <Label> for the tag that already exists in the wishlist
  Then a tag shall not be created under the wishlist <WishlistID>
  And the system shall show the following error message <message>
    Examples:
      | ValidAccountId | WishlistID | Label   | message                                   |
      | 1              | 1          | Toys    | Tag label already exist in this wishlist. |
      | 2              | 2          | Books   | Tag label already exist in this wishlist. |
  
  @Tag
Scenario Outline: User tries to create a tag for a wishlist without proper user permissions
  When the invalid user <InvalidAccountId> in wishlist <WishlistID> enters a valid label <Label>, and a color <Color> for the tag
  Then a tag shall not be created under the wishlist <WishlistID>
  And the system shall show the following error message <message>
    Examples:
      | InvalidAccountId | WishlistID | Label   | Color  | message                                          |
      | 2                | 1          | Music   | Purple | Not authorized to create tags for this wishlist. |
      | 3                | 2          | Food    | Blue   | Not authorized to create tags for this wishlist. |

  @Tag
Scenario Outline: Link permission holder creates a tag successfully
  When the user with valid permission link <ValidPermissionLink> in wishlist <WishlistID> enters a valid label <Label>, and a color <Color> for the tag
  Then a tag with an automatically assigned ID, label <Label>, and color <Color> shall be created under the wishlist <WishlistID>
    Examples:
      | ValidPermissionLink | WishlistID | Label   | Color  |
      | 1                   | 1          | Food    | Red    |
      | 3                   | 3          | Games   | Green  |

  @Tag
Scenario Outline: Link permission holder creates a tag unsuccessfully
  When the user with invalid permission link <InvalidPermissionLink> in wishlist <WishlistID> enters a valid label <Label>, and a color <Color> for the tag
  Then a tag shall not be created under the wishlist <WishlistID>
  And the system shall show the following error message <message>
    Examples:
      | InvalidPermissionLink | WishlistID | Label   | Color  | message                                          |
      | 2                     | 2          | Toys    | Purple | Not authorized to create tags for this wishlist. |
      | 4                     | 4          | Books   | Blue   | Not authorized to create tags for this wishlist. |