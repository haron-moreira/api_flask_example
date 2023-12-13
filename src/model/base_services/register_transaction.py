from src.database.database_connection import Connection
from src.model.base_services.sms_id_register import SMSIdRegister


class Transaction:

    @staticmethod
    def register(body, response, transaction, user_id):
        try:
            dev = Connection.open_connection_dev()

            query = """INSERT INTO sms_register VALUES (
                        0, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s, %s, %s
                        )"""
            valores = (body['name'], body['cost_center'], response['validos'],
                       response['invalidos'], response['repetidos'], response['custo'], user_id, response['id'],
                       body['message'], body['phones'], transaction, 8)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            # rows = cursor.fetchone()

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if SMSIdRegister.register(response['smsIndividuais'], transaction):
                return True

        except Exception as e:
            print(e)
            return False
