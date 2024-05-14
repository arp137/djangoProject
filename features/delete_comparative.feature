Feature: Delete a comparative between two teams
  Scenario: There is a registered user that has created a comparative
    Given Exists a user David
    And User David has created at least one comparative
    Given I login as user "David" with password "Albert2003"
    And I click on the comparative
    And I click on the remove button and I accept to delete it
    Then There is one less comparative