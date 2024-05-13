Feature: Create Comparative

  Scenario: Create a comparative between two teams
    Given I login as user "David" with password "Albert2003"
    When I create a comparative
    Then There are 1 comparative

