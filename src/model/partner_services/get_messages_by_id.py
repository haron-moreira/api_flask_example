from prettyconf import config
import requests


class GetMessagesById:

    @staticmethod
    def Get(id_sms):

        url = config("ENDPOINT_CONSULTA_STATUS").replace("informar_o_smsId", id_sms)

        headers = {
            "Authorization": config("PARTNER_BASIC")
        }

        response = requests.get(url, headers=headers)
        print(response.json())

        status = {
            "não entregue": "fail",
            "entregue no aparelho": "delivered to user phone",
            "enviado para a operadora": "delivered to mobile operator",
            "sem saldo": "no cash to continue",
            "agendado": "scheduled",
            "pausado": "paused",
            "caracteres excedidos": "too many characters",
            "link bloqueado": "invalid URL",
            "falha": "fail",
            "cancelado": "canceled",
            "em processamento": "in process",
            "aguardando processamento": "waiting"
        }

        if response.json()['status'] in status:
            status_resp = status[response.json()['status']]
        else:
            status_resp = "Undefined"

        if response.status_code == 200:
            return {
                "phone": response.json()['numero'],
                "clientId": response.json()['smsClienteId'],
                "smsId": response.json()['smsId'],
                "status": status_resp,
            }
        else:
            return {
                "status": response.status_code
            }
