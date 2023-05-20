import pytest
from controller import MainMenuHandler


@pytest.mark.parametrize(
    "choice,expected",
    [
        ('1', 'viewing_tracked_pods'),
        ('2', 'not_built_yet'),
        ('3', 'not_built_yet'),
        ('4', 'not_built_yet'),
        ('5', 'not_built_yet'),
        ('6', 'not_built_yet'),
        ('7', 'not_built_yet'),
        ('8', 'not_built_yet'),
        ('9', 'not_built_yet'),
        ('q', 'main_menu_goodbye'),
    ],
)
def test_main_menu_with_valid_choices(choice, expected):
    handler = MainMenuHandler()
    assert handler.main_menu(choice=choice, max_attempts=1) == expected

@pytest.mark.parametrize(
    "choice",
    ['invalid', 'v', 'b', '(', '0', '10', 'Q', '!', ' ', '', None],
)
def test_main_menu_with_invalid_choices(choice):
    handler = MainMenuHandler()
    assert handler.main_menu(choice=choice, max_attempts=1) == None

def test_main_menu_with_valid_choice_first_attempt():
    handler = MainMenuHandler()
    choice = '1'
    expected_menu = handler.valid_choices[choice]
    assert handler.main_menu(choice=choice, max_attempts=1) == expected_menu

def test_main_menu_with_invalid_then_valid_choice():
    handler = MainMenuHandler()
    choice_invalid = 'invalid'
    choice_valid = '1'
    expected_menu = handler.valid_choices[choice_valid]
    assert handler.main_menu(choice=[choice_invalid, choice_valid], max_attempts=2) == expected_menu

def test_main_menu_with_invalid_choice_only():
    handler = MainMenuHandler()
    choice_invalid = 'invalid'
    assert handler.main_menu(choice=[choice_invalid, choice_invalid], max_attempts=2) == None
