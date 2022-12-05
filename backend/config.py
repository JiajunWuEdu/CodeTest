class Config():

    BASE_PORT = 8008

    LOG_DIR: str = "logs"

    MYSQL_NAME : str = "mylearning"
    MYSQL_HOST : str = "127.0.0.1"
    MYSQL_PORT : int = 3306
    MYSQL_USERNAME : str = "mylearning"
    MYSQL_PASSWORD : str = "mylearning"

config = Config()