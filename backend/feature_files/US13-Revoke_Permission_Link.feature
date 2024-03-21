Feature: Revoke permission link for a wishlist
  As a wishlist owner,
  I want to be able to revoke a permission link for my wishlist,
  so that I can restrict access to my collaborators and prevent further interactions with my wishlist.

  Background:
    Given there is a user with username "willy_wonka_37@gmail.com", email "willy_wonka_37@gmail.com" and password "g+w'}02g=5"
    And the user owns wishlist "13ec4ce6-94d4-4880-99a8-7f0b5fae1220" with name "ChocolateFactoryGroceryItems-Feb25"
    And there is a permission link e7857438-b195-4ff9-8b39-7c8d4600b648 for the wishlist with permission 0b01001010

  Scenario: Revoke permission link for a wishlist
    Given the user is logged in as owner of the wishlist
    When the user revokes the permission link e7857438-b195-4ff9-8b39-7c8d4600b648
    Then the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 is not available
    And the collaborators using the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 lose access to the wishlist

  Scenario Outline: Revoke permission link for a wishlist with other permission links
    Given the user is logged in as owner of the wishlist
    And there is a permission link <other_link> for the wishlist with permission <other_permission>
    When the user revokes the permission link e7857438-b195-4ff9-8b39-7c8d4600b648
    Then the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 is not available
    And the collaborators using the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 lose access to the wishlist
    And the permission link <other_link> is available
    And the permission link <other_link> has permission <other_permission>

    Examples:
      | other_link                              | other_permission |
      | ada56787-c2b1-4a90-9b32-bb0e33054199    | 0b00000000       |
      | ffda5587-4b66-4f8a-be47-8ead8ed705a7    | 0b01001010       |
      | a68cdaca-cb1c-4090-8e0f-ca27cca59e2e    | 0b01111110       |

  Scenario: Revoke permission link for a wishlist without being owner of the wishlist
    Given the user is not logged in as owner of the wishlist
    When the user revokes the permission link e7857438-b195-4ff9-8b39-7c8d4600b648
    Then the request should fail
    And the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 is available
    And the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 has permission 0b01001010