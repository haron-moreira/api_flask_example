from src.database.database_connection import Connection


class UpdateCampaignStatusToEnd:

    @staticmethod
    def update(id_sms):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT CASE WHEN count(sms_id_register.id_sms_register) = sms_register.qtd_numeros_validos 
            THEN 1 ELSE 0 END as status FROM sms_id_register LEFT JOIN sms_register on (
            sms_id_register.co_sms_register = sms_register.id_registro and sms_status in (3,4,5,8,9,10)) WHERE 
            sms_register.transaction_id = %s GROUP BY 
            sms_id_register.co_sms_register;"""

            valores = (id_sms,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            if rows[0] == 1:
                query = """UPDATE sms_register SET status_envio = 3 WHERE transaction_id = %s;"""

                valores = (id_sms,)

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
