import os

IMAGE_NAME = "knvb-team-2"


def handle_input() -> dict:
    container_name = input("Enter the CONTAINER_NAME: ")
    port = input("Enter the PORT: ")
    mysql_user = input("Enter the MYSQL_USER: ")
    mysql_password = input("Enter the MYSQL_PASSWORD: ")
    mysql_host = input("Enter the MYSQL_HOST: ")
    mysql_db = input("Enter the MYSQL_DB: ")

    return {"container_name": container_name, "port": port,
            "mysql_user": mysql_user, "mysql_password": mysql_password,
            "mysql_host": mysql_host, "mysql_db": mysql_db}


def generate_command(input: dict) -> str:
    return f"docker run -p {input['port']}:5000 \
        -e MYSQL_USER={input['mysql_user']} \
        -e MYSQL_PASSWORD={input['mysql_password']} \
        -e MYSQL_HOST={input['mysql_host']} \
        -e MYSQL_DB={input['mysql_db']} \
        --name {input['container_name']} \
        {IMAGE_NAME}"


def main() -> None:
    input = handle_input()
    os.system(generate_command(input))


if __name__ == '__main__':
    main()
