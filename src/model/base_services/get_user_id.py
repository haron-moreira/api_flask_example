from src.database.database_connection import Connection


class GetUserId:

    @staticmethod
    def get(user_name):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT id FROM user WHERE username = %s"""
            valores = (user_name,)

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
