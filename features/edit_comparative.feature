Feature: Edit a comparative between two Teams
  Scenario: There is a registered user that has created a comparative
    Given Exists a user David
    And User David has created at least one comparative
    Given I login as user "David" with password "Albert2003"
    And I click on the comparative
    And I click on the edit button and accept it
    Then There is the same number of Comparatives, Seasons and Team Stadistics
