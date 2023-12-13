from src.database.database_connection import Connection
import json

class Log:

    @staticmethod
    def register(msg, token, transaction, user, route, method, ip, status):
        try:
            dev = Connection.open_connection_dev()

            json_data = {
                "log_message": msg,
                "token": token,
                "transaction": transaction,
                "user": user,
                "route": route,
                "method": method,
                'ip': ip
            }

            query = """INSERT INTO logger VALUES (0, %s, %s, now());"""
            valores = (json.dumps(json_data), status)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchall()

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            return True

        except Exception as e:
            print(e)
            return False
