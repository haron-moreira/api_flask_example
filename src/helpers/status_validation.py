from src.database.database_connection import Connection


class StatusValidation:

    @staticmethod
    def validate(status_message):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT id FROM status_sms_individual WHERE desc_status_pt_br = %s;"""
            valores = (status_message,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchone()

            if rows is None:
                return 10

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            return rows[0]

        except Exception as e:
            print(e)
            return 10
