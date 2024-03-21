Feature: Create permission link in a wishlist
  As a wishlist owner,
  I want to be able to create a permission link for my wishlist,
  so that I can share it with my collaborators and control what they can do with my wishlist.

  Background:
    Given there is a user with username "willy_wonka_37@gmail.com", email "willy_wonka_37@gmail.com" and password "g+w'}02g=5"
    And the user owns wishlist "13ec4ce6-94d4-4880-99a8-7f0b5fae1220" with name "ChocolateFactoryGroceryItems-Feb25"

  Scenario: Create a permission link for a wishlist
    Given the user is logged in as owner of the wishlist
    When the user creates a permission link for the wishlist without explicitly specifying a permission
    Then a permission link for the wishlist is created with the default permission

  Scenario Outline: Create a permission link for a wishlist with specific permission
    Given the user is logged in as owner of the wishlist
    When the user creates a permission link for the wishlist with permission <permission>
    Then a permission link for the wishlist is created with permission <permission>

    Examples:
      | permission   |
      | 0b00000000   |
      | 0b00000010   |
      | 0b01001010   |
      | 0b01111110   |

  Scenario Outline: Create a permission link for a wishlist with existing permission link
    Given the user is logged in as owner of the wishlist
    And there is a permission link <other_link> for the wishlist with permission <other_permission>
    When the user creates a permission link for the wishlist with permission <permission>
    Then a permission link for the wishlist is created with permission <permission>
    And the permission link <other_link> is available
    And the permission link <other_link> has permission <other_permission>

    Examples:
      | other_link                             | other_permission | permission   |
      | c108434a-20aa-4c26-b041-493994c41332   | 0b00000000       | 0b00000010   |
      | eb1f30b9-043b-4324-86af-887efc4b61a3   | 0b00000010       | 0b01001010   |
      | 40e00000-aeb6-43af-968b-08e04f077e74   | 0b01001010       | 0b01111110   |
      | 1337bd07-1945-4563-a7e2-dd11e94d3dd8   | 0b01111110       | 0b00000000   |

  Scenario Outline: Create a permission link for a wishlist without being owner of the wishlist
    Given the user is not logged in as owner of the wishlist
    When the user creates a permission link for the wishlist with permission <permission>
    Then the request should fail
    And no permission link is created for the wishlist

    Examples:
      | permission   |
      | 0b00000000   |
      | 0b00000010   |
      | 0b01001010   |
      | 0b01111110   |
