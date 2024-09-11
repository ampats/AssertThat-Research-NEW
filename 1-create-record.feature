# language: en
Feature: Create Record

    @MANUAL 
    Scenario Outline: Create a new record
        
        Given I have a valid session id
        When Using <file_name>, to create <object_type> I receive a record id
        And I am logged into Veeva as DEVELOPER
        And I navigate to new record page using its id
        Then I see the record is moved to the <lifecycle_state> Lifecycle state
        Examples:
          | file_name        | object_type        | lifecycle_state |
          | apiMirRecord.csv | quality_event__qdm | Define Team     |

