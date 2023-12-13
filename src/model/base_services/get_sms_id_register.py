from src.database.database_connection import Connection


class GetSmsIdRegister:

    @staticmethod
    def get(transaction):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT sms_id FROM sms_id_register WHERE co_sms_register = 
             (SELECT id_registro FROM sms_register WHERE transaction_id = %s)"""
            valores = (transaction,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchall()
            print(rows)

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if rows is None:
                return 0

            return rows

        except Exception as e:
            print(e)
            return 0
