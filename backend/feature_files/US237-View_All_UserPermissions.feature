Feature: View all UserPermissions
  As a user,
  I want to view all UserPermissions
  so that I can manage who has access to my wishlists.

  Background:
    Given clear test data

  @Linwei @Linwei4
  Scenario Outline: Successfully View all UserPermissions (1) on a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <owner_user_id> attempts to view all UserPermissions with wishlist_id <owner_wishlist_id>
    Then the request returns the status code <status_code>
    And the response is a list of size 1
    And the response is a list of UserPermissions that contains the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email | other_password | permissions | status_code |
      | 1             | owner1         | owner1@com  | password       | 1                 | wishlist1           | 2             | other1         | other1@com  | password       | 1           | 200         |
      | 3             | owner3         | owner3@com  | password       | 3                 | wishlist3           | 4             | other3         | other3@com  | password       | 2           | 200         |
      | 5             | owner5         | owner5@com  | password       | 5                 | wishlist5           | 6             | other5         | other5@com  | password       | 3           | 200         |

  @Linwei @Linwei4
  Scenario Outline: Successfully View all UserPermissions (3) on a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other1_user_id> and username <other1_username> and email <other1_email> and password <other1_password>
    And there is a UserAccount with id <other2_user_id> and username <other2_username> and email <other2_email> and password <other2_password>
    And there is a UserAccount with id <other3_user_id> and username <other3_username> and email <other3_email> and password <other3_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other1_user_id> and permissions <permissions1>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other2_user_id> and permissions <permissions2>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other3_user_id> and permissions <permissions3>
    When the user with id <owner_user_id> attempts to view all UserPermissions with wishlist_id <owner_wishlist_id>
    Then the request returns the status code <status_code>
    And the response is a list of size 3
    And the response is a list of UserPermissions that contains the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other1_user_id> and permissions <permissions1>
    And the response is a list of UserPermissions that contains the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other2_user_id> and permissions <permissions2>
    And the response is a list of UserPermissions that contains the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other3_user_id> and permissions <permissions3>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other1_user_id>
    And delete the UserAccount with id <other2_user_id>
    And delete the UserAccount with id <other3_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other1_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other2_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other3_user_id>
    Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other1_user_id | other1_username | other1_email | other1_password | other2_user_id | other2_username | other2_email | other2_password | other3_user_id | other3_username | other3_email | other3_password | permissions1 | permissions2 | permissions3 | status_code |
      | 1             | owner1         | owner1@com  | password       | 1                 | wishlist1           | 2              | other1          | other1@com   | password        | 3              | other2          | other9@com   | password        | 4              | other4          | other4@com   | password        | 1            | 2            | 3            | 200         |
      | 5             | owner5         | owner5@com  | password       | 5                 | wishlist5           | 6              | other6          | other6@com   | password        | 7              | other7          | other7@com   | password        | 8              | other8          | other8@com   | password        | 1            | 2            | 3            | 200         |
      | 9             | owner9         | owner9@com  | password       | 9                 | wishlist9           | 10             | other10         | other10@com  | password        | 11             | other11         | other11@com  | password        | 12             | other12         | other12@com  | password        | 1            | 2            | 3            | 200         |

  @Linwei @Linwei4
  Scenario Outline: Successfully View all UserPermissions (0) on a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    When the user with id <owner_user_id> attempts to view all UserPermissions with wishlist_id <owner_wishlist_id>
    Then the request returns the status code <status_code>
    And the response is a list of size 0
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | status_code |
      | 1             | owner1         | owner1@com  | password       | 1                 | wishlist1           | 200         |
      | 2             | owner2         | owner2@com  | password       | 2                 | wishlist2           | 200         |
      | 3             | owner3         | owner3@com  | password       | 3                 | wishlist3           | 200         |

  @Linwei @Linwei4
  Scenario Outline: Unsuccessfully View all UserPermissions on a Wishlist that does not exist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    When the user with id <owner_user_id> attempts to view all UserPermissions with wishlist_id <owner_wishlist_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And delete the UserAccount with id <owner_user_id>
    Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | status_code |
      | 1             | owner1         | owner1@com  | password       | 2                 | 400         |
      | 3             | owner3         | owner3@com  | password       | 4                 | 400         |
      | 5             | owner5         | owner5@com  | password       | 6                 | 400         |

  @Linwei @Linwei4
  Scenario Outline: Unsuccessfully View all UserPermissions on a Wishlist You Are Not the Owner Of
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    When the user with id <other_user_id> attempts to view all UserPermissions with wishlist_id <owner_wishlist_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And delete the UserAccount with id <owner_user_id>
    And delete the UserAccount with id <other_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    Examples:
      | owner_user_id | owner_username | owner_email | owner_password | other_user_id | other_username | other_email | other_password | owner_wishlist_id | owner_wishlist_name | status_code |
      | 1             | owner1         | owner1@com  | password       | 2             | other1         | other1@com  | password       | 3                 | wishlist3           | 403         |
      | 4             | owner4         | owner4@com  | password       | 5             | other5         | other5@com  | password       | 6                 | wishlist6           | 403         |
      | 7             | owner7         | owner7@com  | password       | 8             | other8         | other8@com  | password       | 9                 | wishlist9           | 403         |
