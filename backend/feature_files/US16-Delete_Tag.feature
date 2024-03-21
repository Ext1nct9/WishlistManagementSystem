Feature: Delete a tag
  As a user,
  I want to be able to delete an existing tag.
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
Scenario Outline: Delete a tag successfully
  When the valid user <ValidAccountId> in wishlist <WishlistID> in tag <TagID> deletes the tag
  Then the tag shall be deleted successfully
    Examples:
      | ValidAccountId | WishlistID | TagID |
      | 1              | 1          | 1     |
      | 2              | 2          | 2     |
      | 3              | 1          | 1     |
      | 1              | 2          | 2     |

@Tag
Scenario Outline: Delete a tag unsuccessfully
  When the invalid user <InvalidAccountId> in wishlist <WishlistID> in tag <TagID> deletes the tag
  Then the tag shall not be deleted
  And the system shall show the following error message <message>
    Examples:
      | InvalidAccountId | WishlistID | TagID | message                                          |
      | 2                | 1          | 1     | Not authorized to delete tags for this wishlist. |
      | 3                | 2          | 2     | Not authorized to delete tags for this wishlist. |

@Tag
Scenario Outline: Link permission holder deletes a tag successfully
  When the user with valid permission link <ValidPermissionLink> in wishlist <WishlistID> in tag <TagID> deletes the tag
  Then the tag shall be deleted successfully
    Examples:
      | ValidPermissionLink | WishlistID | TagID |
      | 1                   | 1          | 1     |
      | 3                   | 3          | 3     |

@Tag
Scenario Outline: Link permission holder deletes a tag unsuccessfully
  When the user with invalid permission link <InvalidPermissionLink> in wishlist <WishlistID> in tag <TagID> deletes the tag
  Then the tag shall not be deleted
  And the system shall show the following error message <message>
    Examples:
      | InvalidPermissionLink | WishlistID | TagID | message                                          |
      | 2                     | 2          | 2     | Not authorized to delete tags for this wishlist. |
      | 4                     | 4          | 4     | Not authorized to delete tags for this wishlist. |
