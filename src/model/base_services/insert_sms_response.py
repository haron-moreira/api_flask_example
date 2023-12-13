from src.database.database_connection import Connection


class InsertSmsResponse:

    @staticmethod
    def insert(id_sms, response):
        try:
            dev = Connection.open_connection_dev()

            query = """INSERT INTO sms_resposta VALUES (0, (SELECT id_sms_register FROM sms_id_register WHERE sms_id 
            = %s), %s)"""
            valores = (id_sms, response)

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
