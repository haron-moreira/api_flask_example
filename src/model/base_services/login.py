from src.database.database_connection import Connection


class Login:

    @staticmethod
    def login(username, password):
        try:
            dev = Connection.open_connection_dev()

            query = "select id from user where username = %s and password = %s"
            valores = (username, password)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if rows is None:
                return False

            return True

        except Exception as e:
            print(e)
            return None
