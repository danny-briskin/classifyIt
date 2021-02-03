@images

Feature: Images validation

#  Background:
#    Given I load OpenCV library

  Scenario Outline: Classification of images on QAC website
    Given I load webdriver
    Given I open "<PAGE>"
    When I find all images on the page
    #And I grab all text from the page
    #Then I run classification
    Then I close webdriver

    Examples:
      | PAGE           |
#      | industries/healthcare/ |
#      | old-home-page/         |
#      | about-us/careers/      |
#      | category/blog/ |
#|                /|
  |                solutions-and-services/test-automation/|


#    Scenario: Teardown
#        Given I close webdriver