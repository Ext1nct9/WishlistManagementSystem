Feature: Update a tag
  As a user,
  I want to be able to update the information of an existing tag,
  So that I can manage the tags that categorize the items in my wishlist.

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
Scenario Outline: Update a tag successfully
  When the valid user <ValidAccountId> in wishlist <WishlistID> in tag <TagID> enters a valid label <Label>, and a color <Color> to update the tag
  Then the tag <TagID> shall be updated to have label <Label> and color <Color>
    Examples:
      | ValidAccountId | WishlistID | TagID | Label  | Color  |
      | 1              | 1          | 1     | Toys   | Green  |
      | 2              | 2          | 2     | Games  | Red    |
      | 3              | 1          | 1     | Music  | Blue   |
      | 1              | 2          | 2     | Food   | Purple |

 @Tag
Scenario Outline: Update a tag with no color input
  When the valid user <ValidAccountId> in wishlist <WishlistID> in tag <TagID> enters a valid label <Label>, and no color to update the tag
  Then the tag <TagID> shall be updated to have label <Label> and a random color
    Examples:
      | ValidAccountId | WishlistID | TagID | Label  | 
      | 1              | 1          | 1     | Toys   |
      | 2              | 2          | 2     | Games  |

 @Tag
Scenario Outline: Update a tag with no label input
  When the valid user <ValidAccountId> in wishlist <WishlistID> in tag <TagID> enters no label, and a color <Color> to update the tag
  Then the tag shall not be updated
  And the system shall show the following error message <message>
    Examples:
      | ValidAccountId | WishlistID | TagID | Color | message                    |
      | 1              | 1          | 1     | Green | Tag label cannot be blank. |
      | 2              | 2          | 2     | Red   | Tag label cannot be blank. |

 @Tag
Scenario Outline: Update a tag without the proper user permissions
  When the invalid user <InvalidAccountId> in wishlist <WishlistID> in tag <TagID> enters a valid label <Label>, and a color <Color> to update the tag
  Then the tag shall not be updated
  And the system shall show the following error message <message>
    Examples:
    | InvalidAccountId | WishlistID | TagID | Label   | Color  | message                                          |
    | 2                | 1          | 1     | Music   | Purple | Not authorized to update tags for this wishlist. |
    | 3                | 2          | 2     | Food    | Blue   | Not authorized to update tags for this wishlist. | 

 @Tag
Scenario Outline: Link permission holder updates a tag successfully
  When the user with valid permission link <ValidPermissionLink> in wishlist <WishlistID> in tag <TagID> enters a valid label <Label>, and a color <Color> to update the tag
  Then the tag <TagID> shall be updated to have label <Label> and color <Color>
    Examples:
      | ValidPermissionLink | WishlistID | TagID | Label   | Color  |
      | 1                   | 1          | 1     | Food    | Red    |
      | 3                   | 3          | 3     | Games   | Green  |

 @Tag
Scenario Outline: Link permission holder updates a tag unsuccessfully
  When the user with invalid permission link <InvalidPermissionLink> in wishlist <WishlistID> in tag <TagID> enters a valid label <Label>, and a color <Color> to update the tag
  Then the tag shall not be updated
  And the system shall show the following error message <message>
    Examples:
      | InvalidPermissionLink | WishlistID | TagID | Label   | Color  | message                                          |
      | 2                     | 2          | 2     | Toys    | Purple | Not authorized to update tags for this wishlist. |
      | 4                     | 4          | 4     | Books   | Blue   | Not authorized to update tags for this wishlist. |