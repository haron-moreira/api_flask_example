from src.database.database_connection import Connection


class GetSmsByDate:

    @staticmethod
    def get(dt_inicial, dt_final, username):
        try:
            dev = Connection.open_connection_dev()

            query = """SELECT sms_register.nome_campanha as name, sms_register.centro_custo as cost_center, 
            sms_register.qtd_numeros_validos as valid_numbers, sms_register.qtd_numeros_invalidos as invalid_numbers, 
            sms_register.qtd_numeros_repetidos as repeated_numbers, sms_register.data_envio as register_date, 
            sms_register.id_campanha as id, user.username as sender, sms_register.mensagem_enviada as message, 
            sms_register.numeros_sms as numbers, sms_register.transaction_id as transaction, status_campanha.desc_envio 
            as status FROM sms_register LEFT JOIN status_campanha ON (sms_register.status_envio = 
            status_campanha.idstatus_envio) LEFT JOIN user ON (user.id = sms_register.user_envio) WHERE 
            (sms_register.data_envio BETWEEN %s AND %s) AND sms_register.user_envio = %s;"""
            valores = (dt_inicial, dt_final, username)

            cursor = dev.cursor()
            cursor.execute(query, valores)
            rows = cursor.fetchall()
            # print(rows)

            result_list = []

            for row in rows:
                result_dict = {}
                for column_name, value in zip(cursor.description, row):
                    result_dict[column_name[0]] = value
                result_list.append(result_dict)

            # print(result_list)

            dev.commit()
            dev.close()
            Connection.close_connection(dev)

            if rows is None:
                return 0

            if len(rows) == 0:
                return 0

            return result_list

        except Exception as e:
            print(e)
            return 0
