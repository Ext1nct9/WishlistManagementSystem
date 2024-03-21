Feature: Update permission link in a wishlist
  As a wishlist owner,
  I want to be able to modify the permissions associated with a permission link for my wishlist,
  so that I can adjust the level of access granted to my collaborators at any time.

  Background:
    Given there is a user with username "willy_wonka_37@gmail.com", email "willy_wonka_37@gmail.com" and password "g+w'}02g=5"
    And the user owns wishlist "13ec4ce6-94d4-4880-99a8-7f0b5fae1220" with name "ChocolateFactoryGroceryItems-Feb25"
    And there is a permission link e7857438-b195-4ff9-8b39-7c8d4600b648 for the wishlist with permission 0b01001010

  Scenario Outline: Update permission link for a wishlist
    Given the user is logged in as owner of the wishlist
    When the user updates the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 with permission <permission>
    Then the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 is updated with permission <permission>
    And the collaborators using the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 has the permission <permission>

    Examples:
      | permission   |
      | 0b00000000   |
      | 0b00000010   |
      | 0b01111010   |
      | 0b01111110   |

  Scenario Outline: Update permission link for a wishlist with other permission links
    Given the user is logged in as owner of the wishlist
    And there is a permission link <other_link> for the wishlist with permission <other_permission>
    When the user updates the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 with permission <updated_permission>
    Then the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 is updated with permission <updated_permission>
    And the collaborators using the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 has the permission <updated_permission>
    And the permission link <other_link> has permission <other_permission>

    Examples:
      | other_link                               | other_permission | updated_permission |
      | "73531d6d-d3d5-466f-9706-aeec7e74b1c5"   | 0b01001010       | 0b00000010         |
      | "8925055b-4438-41b8-96c2-b31353c2f516"   | 0b01001010       | 0b01111110         |
      | "8527c62e-9f24-41dc-bd1e-09652d1921cc"   | 0b01001010       | 0b00000010         |
      | "60f60bf0-401d-4ab3-b12a-7b0eb09d9a4d"   | 0b01111110       | 0b01111110         |

  Scenario Outline: Update permission link for a wishlist without being owner of the wishlist
    Given the user is not logged in as owner of the wishlist
    When the user updates the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 with permission <permission>
    Then the request should fail
    And the permission link e7857438-b195-4ff9-8b39-7c8d4600b648 has permission 0b01001010

    Examples:
      | permission   |
      | 0b00000000   |
      | 0b00000010   |
      | 0b01111010   |
      | 0b01111110   |