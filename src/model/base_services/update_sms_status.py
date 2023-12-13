from src.database.database_connection import Connection


class UpdateSmsStatus:

    @staticmethod
    def update(id_sms, status, operadora):
        try:
            dev = Connection.open_connection_dev()

            query = """UPDATE sms_id_register SET operadora = %s, sms_status = %s, dt_last_update = now()
                        WHERE sms_id = %s;"""
            valores = (operadora, status, id_sms)

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
