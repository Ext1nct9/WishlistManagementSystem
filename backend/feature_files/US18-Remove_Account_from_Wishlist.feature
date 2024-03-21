Feature: Revoke an account's permissions on a wishlist
  As a user,
  I want to revoke an account's permissions on my wishlist.
  So that I can manage other people's access permissions on my wishlists.

  Background:
    Given clear test data

  @Linwei @Linwei2
  Scenario Outline: Successfully Remove a User from a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <owner_user_id> attempts to remove the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And there does not exist a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
      | owner_user_id | owner_username | owner_email      | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | permissions | status_code |
      | 1             | owner1         | owner1@email.com | password1      | 1                 | wishlist1           | 2             | other1         | other1@email.com | password2      | 1           | 204         |
      | 3             | owner2         | owner2@email.com | password2      | 2                 | wishlist2           | 4             | other2         | other2@email.com | password3      | 2           | 204         |
      | 5             | owner3         | owner3@email.com | password3      | 3                 | wishlist3           | 6             | other3         | other3@email.com | password4      | 3           | 204         |

  @Linwei @Linwei2
  Scenario Outline: Unsuccessfully Remove a Non-Existent User from a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    When the user with id <owner_user_id> attempts to remove the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <non_existent_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there does not exist a UserPermission with wishlist_id <owner_wishlist_id> and user_id <non_existent_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
      Examples:
      | owner_user_id | owner_username | owner_email      | owner_password | owner_wishlist_id | owner_wishlist_name | non_existent_user_id | status_code |
      | 1             | owner1         | owner1@email.com | password1      | 1                 | wishlist1           | 2                    | 400         |
      | 3             | owner2         | owner2@email.com | password2      | 2                 | wishlist2           | 4                    | 400         |
      | 5             | owner3         | owner3@email.com | password3      | 3                 | wishlist3           | 6                    | 400         |

  @Linwei @Linwei2
  Scenario Outline: Unsuccessfully Remove a User from a Wishlist You Are Not the Owner Of
    Given there is a UserAccount with id <fake_owner_user_id> and username <owner_username> and email <fake_owner_email> and password <fake_owner_password>
    And there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <fake_owner_user_id> attempts to remove the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there exists a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    And delete the UserAccount with id <fake_owner_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
      | fake_owner_user_id | fake_owner_username | fake_owner_email      | fake_owner_password | owner_user_id | owner_username | owner_email      | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | permissions | status_code |
      | 1                  | fake_owner1         | fake_owner1@email.com | password1           | 2             | owner1         | owner1@email.com | password2      | 1                 | wishlist1           | 3             | other1         | other1@email.com | password3      | 1           | 403         |
      | 3                  | fake_owner2         | fake_owner2@email.com | password2           | 4             | owner2         | owner2@email.com | password4      | 2                 | wishlist2           | 5             | other2         | other2@email.com | password5      | 2           | 403         |
      | 5                  | fake_owner3         | fake_owner3@email.com | password3           | 6             | owner3         | owner3@email.com | password6      | 3                 | wishlist3           | 7             | other3         | other3@email.com | password7      | 3           | 403         |

  @Linwei @Linwei2
  Scenario Outline: Unsuccessfully Remove a User's Access to a Wishlist They Do Not Have Access To
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    When the user with id <owner_user_id> attempts to remove the UserPermission to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there does not exist a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
      Examples:
      | owner_user_id | owner_username | owner_email      | owner_password | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | status_code |
      | 1             | owner1         | owner1@email.com | password1      | 1                 | wishlist1           | 2             | other1         | other1@email.com | password2      | 400         |
      | 3             | owner2         | owner2@email.com | password2      | 2                 | wishlist2           | 4             | other2         | other2@email.com | password3      | 400         |
      | 5             | owner3         | owner3@email.com | password3      | 3                 | wishlist3           | 6             | other3         | other3@email.com | password4      | 400         |
