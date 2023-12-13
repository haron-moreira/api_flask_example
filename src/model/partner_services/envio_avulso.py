import requests
from prettyconf import config

from src.helpers.valida_centro_custo import ValidaCentroCusto


class EnvioAvulso:

    @staticmethod
    def send_message(numeros: list, mensagem: str, nome_da_campanha: str, centro_custo: str,
                     urlCallBackEntrega: str, urlCallBackResposta: str,
                     agendamentos=None, smsClientId: str = "", whatsappId: str = ""):

        if agendamentos is None:
            agendamentos = []

        url = config("ENDPOINT_ENVIO_AVULSO")
        product_id = ValidaCentroCusto.getProductId(centro_custo)

        if len(numeros) == 1:
            numero = numeros[0]
        else:
            numero = str(numeros).replace(",", " ")

        payload = {
            "agendamentos": agendamentos,
            "centroCustoId": centro_custo,
            "envios": [
                {
                    "mensagemNumero": mensagem,
                    "numero": numero,
                    "smsClienteId": smsClientId

                }
            ],
            "mensagemCampanha": mensagem,
            "nome": nome_da_campanha,
            "produtoId": product_id,
            "telefones": numero,
            "urlCallbackEntrega": urlCallBackEntrega,
            "urlCallbackResposta": urlCallBackResposta,
            "whatsappId": whatsappId
        }

        headers = {
            "Authorization": config("PARTNER_BASIC")
        }

        print(payload)
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())

        if response.status_code == 200:
            return {
                'id': response.json()['id'],
                'invalidos': response.json()['invalidos'],
                'repetidos': response.json()['repetidos'],
                'validos': response.json()['validos'],
                'custo': response.json()['custo'],
                "smsIndividuais": response.json()['smsEnvios']
            }
        else:
            return {
                "id": None
            }
