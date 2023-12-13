from prettyconf import config
import mysql.connector


class Connection:

    @staticmethod
    def open_connection_dev():
        try:
            connection = mysql.connector.connect(
                host=config("DATABASE_HOST"),
                user=config("DATABASE_USER"),
                password=config("DATABASE_PASSWORD"),
                database=config("DATABASE_DB_NAME"),
            )
            return connection

        except Exception as e:
            return None

    @staticmethod
    def close_connection(connection):
        connection.close()
