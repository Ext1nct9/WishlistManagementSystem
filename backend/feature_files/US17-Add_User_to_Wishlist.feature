Feature: Give an account permissions to a wishlist
  As a user,
  I want to add an account to my wishlist.
  So that I can manage other people's access permissions on my wishlists.

  Background:
    Given clear test data

  @Linwei @Linwei1
  Scenario Outline: Successfully Add a User to a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    When the user with id <owner_user_id> attempts to add a new UserPermission with permissions <permissions> to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And there exists a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
        | owner_user_id | owner_username | owner_email      | owner_password  | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | permissions | status_code |
        | 1             | owner_name1    | owner1@email.com | owner_password1 | 1                 | wishlist_name1      | 2             | other_name1    | other1@email.com | other_password | 1           | 201         |
        | 3             | owner_name2    | owner2@email.com | owner_password2 | 2                 | wishlist_name2      | 4             | other_name2    | other2@email.com | other_password | 2           | 201         |
        | 5             | owner_name3    | owner3@email.com | owner_password3 | 3                 | wishlist_name3      | 6             | other_name3    | other3@email.com | other_password | 3           | 201         |

  @Linwei
  Scenario Outline: Unsuccessfully Add a Non-Existent User to a Wishlist
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    When the user with id <owner_user_id> attempts to add a new UserPermission with permissions <permissions> to the Wishlist with id <owner_wishlist_id> for the user with id <non_existent_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there does not exist a UserPermission with wishlist_id <owner_wishlist_id> and user_id <non_existent_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
      Examples:
        | owner_user_id | owner_username | owner_email      | owner_password  | owner_wishlist_id | owner_wishlist_name | non_existent_user_id | permissions | status_code |
        | 1             | owner_name1    | owner1@email.com | owner_password1 | 1                 | wishlist_name1      | 2                    | 1           | 400         |
        | 3             | owner_name2    | owner2@email.com | owner_password2 | 2                 | wishlist_name2      | 4                    | 2           | 400         |
        | 5             | owner_name3    | owner3@email.com | owner_password3 | 3                 | wishlist_name3      | 6                    | 3           | 400         |

  @Linwei @Linwei1
  Scenario Outline: Unsuccessfully Add a User to a Wishlist You Are Not the Owner Of
    Given there is a UserAccount with id <fake_owner_user_id> and username <fake_owner_username> and email <fake_owner_email> and password <fake_owner_password>
    And there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    When the user with id <fake_owner_user_id> attempts to add a new UserPermission with permissions <permissions> to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there does not exist a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    And delete the UserAccount with id <fake_owner_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
      Examples:
        | fake_owner_user_id | fake_owner_username | fake_owner_email      | fake_owner_password  | owner_user_id | owner_username | owner_email      | owner_password  | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | permissions | status_code |
        | 1                  | fake_owner_name1    | fake_owner1@email.com | fake_owner_password1 | 2             | owner_name1    | owner1@email.com | owner_password1 | 1                 | wishlist_name1      | 3             | other_name1    | other1@email.com | other_password | 1           | 403         |
        | 4                  | fake_owner_name2    | fake_owner2@email.com | fake_owner_password2 | 5             | owner_name2    | owner2@email.com | owner_password2 | 2                 | wishlist_name2      | 6             | other_name2    | other2@email.com | other_password | 2           | 403         |
        | 7                  | fake_owner_name3    | fake_owner3@email.com | fake_owner_password3 | 8             | owner_name3    | owner3@email.com | owner_password3 | 3                 | wishlist_name3      | 9             | other_name3    | other3@email.com | other_password | 3           | 403         |

  @Linwei @Linwei1
  Scenario Outline: Unsuccessfully Add a User to a Wishlist the User is Already In
    Given there is a UserAccount with id <owner_user_id> and username <owner_username> and email <owner_email> and password <owner_password>
    And there is a Wishlist with id <owner_wishlist_id> and name <owner_wishlist_name> and owner_id <owner_user_id>
    And there is a UserAccount with id <other_user_id> and username <other_username> and email <other_email> and password <other_password>
    And there is a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id> and permissions <permissions>
    When the user with id <owner_user_id> attempts to add a new UserPermission with permissions <permissions> to the Wishlist with id <owner_wishlist_id> for the user with id <other_user_id>
    Then the request returns the status code <status_code>
    And the response contains an error message
    And there exists a UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
    And delete the UserAccount with id <owner_user_id>
    And delete the Wishlist with id <owner_wishlist_id>
    And delete the UserAccount with id <other_user_id>
    And delete the UserPermission with wishlist_id <owner_wishlist_id> and user_id <other_user_id>
      Examples:
        | owner_user_id | owner_username | owner_email      | owner_password  | owner_wishlist_id | owner_wishlist_name | other_user_id | other_username | other_email      | other_password | permissions | status_code |
        | 1             | owner_name1    | owner1@email.com | owner_password1 | 1                 | wishlist_name1      | 2             | other_name1    | other1@email.com | other_password | 1           | 400         |
        | 3             | owner_name2    | owner2@email.com | owner_password2 | 2                 | wishlist_name2      | 4             | other_name2    | other2@email.com | other_password | 2           | 400         |
        | 5             | owner_name3    | owner3@email.com | owner_password3 | 3                 | wishlist_name3      | 6             | other_name3    | other3@email.com | other_password | 3           | 400         |
