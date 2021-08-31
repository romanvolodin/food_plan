import argparse
from json.decoder import JSONDecodeError

from environs import Env

from menu import create_week_menu, read_json_file, save_json_file, print_menu


SAVED_WEEKLY_MENU_PATH = "week_menu.json"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "The script allows you to generate a week meal menu. "
            "Also it can generate a shopping list for the menu "
            "and display an instructions for the today meal."
        )
    )
    parser.add_argument(
        "--show-menu",
        help="Shows a saved menu.",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--show-shopping-list",
        help="Shows a shopping list for the saved menu.",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--show-instructions",
        help="Shows an instruction for today meals.",
        type=bool,
        default=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    api_key = env.str("SPOONACULAR_TOKEN")

    args = parse_arguments()
    show_menu = args.show_menu
    show_shopping_list = args.show_shopping_list
    show_instructions = args.show_instructions

    try:
        menu = read_json_file(SAVED_WEEKLY_MENU_PATH)
    except (FileNotFoundError, JSONDecodeError):
        menu = create_week_menu(api_key)
        save_json_file(SAVED_WEEKLY_MENU_PATH, menu)

    print_menu(menu)
