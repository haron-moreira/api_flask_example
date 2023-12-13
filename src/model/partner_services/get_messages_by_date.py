from prettyconf import config
import requests
from urllib.parse import quote


class GetMessagesByDate:

    @staticmethod
    def Get(dt_inicio, dt_final):

        url = config("END_POINT_CONSULTA_BY_DATE") + f"""dataInicial={quote(dt_inicio)}&dataFinal={quote(dt_final)}"""

        headers = {
            "Authorization": config("PARTNER_BASIC")
        }

        response = requests.get(url, headers=headers)
        json_retorno = []
        json_response = response.json()

        json_translate = {
            "centroCusto": "cost_center",
            "dataHoraDisparo": "send_time",
            "dataHoraUpdate": "update_time",
            "nomeCampanha": "campaign_name",
            "telefone": "phone"
        }

        for item in json_response:
            json_temporary = {}
            for key in item:
                if key in json_translate:
                    json_temporary[json_translate[key]] = item[key]
            json_retorno.append(json_temporary)

        if response.status_code == 200:
            return json_retorno

        else:
            return {
                "status": response.status_code
            }
