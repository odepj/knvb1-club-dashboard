import os


def handle_mysql_input() -> dict:
    image_name = input("Enter the IMAGE_NAME: ")
    container_name = input("Enter the CONTAINER_NAME: ")
    port = input("Enter the PORT: ")
    mysql_user = input("Enter the MYSQL_USER: ")
    mysql_password = input("Enter the MYSQL_PASSWORD: ")
    mysql_host = input("Enter the MYSQL_HOST: ")
    mysql_db = input("Enter the MYSQL_DB: ")

    return {"image_name": image_name, "container_name": container_name,
            "port": port, "mysql_user": mysql_user, "mysql_password": mysql_password,
            "mysql_host": mysql_host, "mysql_db": mysql_db}


def handle_mssql_input() -> dict:
    image_name = input("Enter the IMAGE_NAME: ")
    container_name = input("Enter the CONTAINER_NAME: ")
    port = input("Enter the PORT: ")
    azure_db = input("Enter the AZURE_DB: ")

    return {"image_name": image_name, "container_name": container_name,
            "port": port, "azure_db": azure_db}


def generate__mysql_command(input: dict) -> str:
    return f"docker run -p {input['port']}:5000 \
        -e MYSQL_USER={input['mysql_user']} \
        -e MYSQL_PASSWORD={input['mysql_password']} \
        -e MYSQL_HOST={input['mysql_host']} \
        -e MYSQL_DB={input['mysql_db']} \
        --name {input['container_name']} \
        {input['image_name']}"


def generate__mssql_command(input: dict) -> str:
    return f"docker run -p {input['port']}:5000 \
        -e AZURE_DB={input['azure_db']} \
        --name {input['container_name']} \
        {input['image_name']}"


def mysql() -> None:
    input = handle_mysql_input()
    os.system(generate__mysql_command(input))


def mssql() -> None:
    input = handle_mssql_input()
    os.system(generate__mssql_command(input))


def main() -> None:
    type = input("MYSQL(1) or MSSQL(2):  ")

    if type == "1" or type == "MYSQL":
        mysql()
    elif type == "2" or type == "MSSQL":
        mssql()
    return


if __name__ == '__main__':
    main()
