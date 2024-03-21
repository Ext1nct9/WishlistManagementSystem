Feature: Delete a comment
As a wishlist owner, 
I want to be able to delete a comment on an item
So that I can remove unecessary messages on my wishlists.

  Background:
    Given the wishlist 123 has an item 546

  Scenario: Delete a comment on an item
    Given the user is owner of comment 1 on 546
    When the user deletes comment 1
    Then the comment 1 is removed from the database
