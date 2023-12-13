import datetime
import hashlib


class TransactionGenerate:

    @staticmethod
    def generate(texto_base):
        texto = "WaveMessage" + texto_base
        timestamp_atual = str(int(datetime.datetime.now().timestamp()))

        concatenado = texto + timestamp_atual

        md5 = hashlib.md5()
        md5.update(concatenado.encode('utf-8'))

        return md5.hexdigest()
