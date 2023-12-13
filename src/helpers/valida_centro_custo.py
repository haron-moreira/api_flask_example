from src.database.database_connection import Connection


class ValidaCentroCusto:

    @staticmethod
    def getProductId(num_centro_custo):
        try:
            dev = Connection.open_connection_dev()

            query = "select productId from centroDeCusto where num_centroDeCusto = %s"
            valores = (num_centro_custo,)

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
