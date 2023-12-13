from src.database.database_connection import Connection


class SMSIdRegister:

    @staticmethod
    def register(bodySmsIndividual, transaction):
        try:
            dev = Connection.open_connection_dev()

            for sms in bodySmsIndividual:
                query = """INSERT INTO sms_id_register VALUES (
                            0, (SELECT id_registro FROM sms_register WHERE transaction_id = %s), %s, %s, 7, NULL,NULL
                            )"""
                valores = (transaction, sms['numero'], sms['smsId'])

                cursor = dev.cursor()
                cursor.execute(query, valores)

                dev.commit()

            dev.close()
            Connection.close_connection(dev)
            return True

        except Exception as e:
            print(e)
            return False
