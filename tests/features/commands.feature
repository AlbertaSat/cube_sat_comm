Feature: Command execution

    Background:
        Given the command infrastructure has been initialized with test commands

    Scenario: Executing a command that doesn't exist
        When the command "some_command_that_doesn't_exist" is executed
        Then an error should be returned

    Scenario: Executing a command that does exist
        When the command "generic_mock_cmd" is executed
        Then the command should execute with no errors

    Scenario: Executing a command should run the command's script file
        When the command "generic_mock_cmd" is executed
        Then the script file should be run