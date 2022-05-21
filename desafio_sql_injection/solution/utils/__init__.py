import os
from .bcolors import BColors
from bs4 import BeautifulSoup


def render_menu(title_item, options, input_message=None) -> str:
    while True:
        if os.system("cls"):
            os.system("clear")

        print(BColors.OKGREEN + f"{title_item}" + BColors.ENDC)
        print()
        for option in options:
            print(BColors.BOLD, end="")
            print(option)
            print(BColors.ENDC, end="")

        if input_message:
            print()
            choosed = input(input_message)

            if choosed in options:
                return choosed

            print(
                BColors.FAIL
                + "Invalid option! Please type exactly as you see fit."
                + BColors.ENDC
            )
            input("\nPress any key to continue.. ")
        else:
            break

    return ""


def get_form_return(text, **kwargs):
    response = BeautifulSoup(text, "html.parser")

    tabulated_response = []
    for item in response.findAll("pre"):
        resp = {}
        if kwargs.get("first_name"):
            resp[kwargs["first_name"]] = item.text.split("First name: ")[-1]
            resp[kwargs["first_name"]] = resp[kwargs["first_name"]].split("Surname")[0]
        if kwargs.get("surname"):
            resp[kwargs["surname"]] = item.text.split("Surname: ")[-1]

        tabulated_response.append(resp)

    return tabulated_response