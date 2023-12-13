from src.database.database_connection import Connection


class IpValidation:

    @staticmethod
    def validate(transaction):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT count(ip) FROM ip_user_access WHERE ip = %s"""
            valores = (transaction,)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchall()
            # print(rows)

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if rows is None:
                return False

            if int(rows[0][0]) >= 1:
                return True

            return False

        except Exception as e:
            print(e)
            return False
