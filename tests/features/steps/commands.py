from behave import given, when, then
from unittest import mock

from cube_sat_comm import commands
from cube_sat_comm import drawing


_FAKE_COMMANDS_PATH = "tests/other/test_commands/"


@given('the command infrastructure has been initialized with test commands')
def step_impl(_):
    drawing.curses_print = mock.MagicMock()
    commands.init_commands(_FAKE_COMMANDS_PATH)


@when('the command "{cmd_name}" is executed')
def step_impl(context, cmd_name):
    context.script_was_run = False
    context.res = commands.execute_command(cmd_name, lambda: _script_was_run_callback(context))


@then('an error should be returned')
def step_impl(context):
    assert context.res.is_err()



@then('the command should execute with no errors')
def step_impl(context):
    assert context.res.is_ok()


@then('the script file should be run')
def step_impl(context):
    assert context.script_was_run


def _script_was_run_callback(context):
    context.script_was_run = True
