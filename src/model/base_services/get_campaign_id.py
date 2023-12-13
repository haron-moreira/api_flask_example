from src.database.database_connection import Connection


class CampaignId:

    @staticmethod
    def get(transaction, param_type):
        try:
            dev = Connection.open_connection_dev()

            query = """UPDATE sms_register SET status_envio = %s WHERE transaction_id = %s"""
            valores = (param_type, transaction)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            dev.commit()

            query = """SELECT id_campanha FROM sms_register WHERE transaction_id = %s"""
            valores = (transaction,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if rows is None:
                return 0

            # print(rows[0])
            return rows[0]

        except Exception as e:
            print(e)
            return 0
