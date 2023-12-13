from src.database.database_connection import Connection


class UpdateCampaignStatus:

    @staticmethod
    def update(id_sms):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT * FROM sms_register WHERE status_envio = 1 and id_registro = (SELECT co_sms_register FROM 
                        sms_id_register WHERE sms_id = %s);"""

            valores = (id_sms,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            if rows is None:
                return True

            if rows[0] != 0 or rows is not None:
                query = """UPDATE sms_register SET status_envio = 2 WHERE id_registro = (SELECT co_sms_register FROM 
                            sms_id_register WHERE sms_id = %s);"""

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
