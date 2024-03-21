Feature: Update an account's permissions on a wishlist
  As a user,
  I want to update an account's permissions on my wishlist.
  So that I can manage other people's access permissions on my wishlists.

  Background:
    Given clear test data

  @Linwei @Linwei3
  Scenario Outline: Successfully Update a User's Permissions on a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <owner_user_id> attempts to update the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id> to have permissions <new_permissions>
    Then the request returns the status code <status_code>
    And there exists a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <new_permissions>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email | other_password | permissions | new_permissions | status_code |
      | 1             | owner1         | owner1@abc  | password1      | 1                 | wishlist1           | 2             | other1         | other1@abc  | password2      | 1           | 4               | 200         |
      | 3             | owner2         | owner2@abc  | password1      | 2                 | wishlist2           | 4             | other2         | other2@abc  | password2      | 2           | 5               | 200         |
      | 5             | owner3         | owner3@abc  | password1      | 3                 | wishlist3           | 6             | other3         | other3@abc  | password2      | 3           | 6               | 200         |

  @Linwei @Linwei3
  Scenario Outline: Unsuccessfully Update a Non-Existent User's Permissions on a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    When the user with id <owner_user_id> attempts to update the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id> to have permissions <new_permissions>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
      Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | new_permissions | status_code |
      | 1             | owner1         | owner1@abc  | password1      | 1                 | wishlist1           | 2             | 4               | 400         |
      | 3             | owner2         | owner2@abc  | password1      | 2                 | wishlist2           | 4             | 5               | 400         |
      | 5             | owner3         | owner3@abc  | password1      | 3                 | wishlist3           | 6             | 6               | 400         |

  @Linwei @Linwei3
  Scenario Outline: Unsuccessfully Update a User's Access to a Wishlist You Are Not the Owner Of
    Given there is a UserAccount with id <fake_owner_user_id> and username <fake_owner_username> and email <fake_owner_email> and password <fake_owner_password>
    And there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <fake_owner_user_id> attempts to update the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id> to have permissions <new_permissions>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And delete the UserAccount with id <fake_owner_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
      | fake_owner_user_id | fake_owner_username | fake_owner_email | fake_owner_password | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email | other_password | permissions | new_permissions | status_code |
      | 1                  | fake_owner1          | fake_owner1@abc  | password1           | 2             | owner1         | owner1@abc  | password2      | 1                 | wishlist1           | 3             | other1         | other1@abc  | password3      | 1           | 4               | 403         |
      | 3                  | fake_owner2          | fake_owner2@abc  | password1           | 4             | owner2         | owner2@abc  | password2      | 2                 | wishlist2           | 5             | other2         | other2@abc  | password3      | 2           | 5               | 403         |
      | 5                  | fake_owner3          | fake_owner3@abc  | password1           | 6             | owner3         | owner3@abc  | password2      | 3                 | wishlist3           | 7             | other3         | other3@abc  | password3      | 3           | 6               | 403         |

  @Linwei @Linwei3
  Scenario Outline: Unsuccessfully Update a User's Access to a Wishlist They Do Not Have Access To
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    When the user with id <owner_user_id> attempts to update the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id> to have permissions <new_permissions>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
      Examples:
      | owner_user_id | owner_username | owner_email | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | new_permissions | status_code |
      | 1             | owner1         | owner1@abc  | password1      | 1                 | wishlist1           | 2             | 4               | 400         |
      | 3             | owner2         | owner2@abc  | password1      | 2                 | wishlist2           | 4             | 5               | 400         |
      | 5             | owner3         | owner3@abc  | password1      | 3                 | wishlist3           | 6             | 6               | 400         |
