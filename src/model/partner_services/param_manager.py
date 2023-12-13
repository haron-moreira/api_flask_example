import requests
from prettyconf import config
from src.model.base_services.get_campaign_id import CampaignId


class ParamManager:

    @staticmethod
    def manager(param, transaction):
        response = ""
        url = config("END_POINT_CAMPANHA")
        headers = {
            "Authorization": config("PARTNER_BASIC")
        }

        if param == "start":
            campaign_id = CampaignId.get(transaction, 1)
            url += f"iniciar/{campaign_id}"
            response = requests.put(url, headers=headers)
        elif param == "pause":
            campaign_id = CampaignId.get(transaction, 5)
            url += f"pausar/{campaign_id}"
            response = requests.put(url, headers=headers)
        elif param == "cancel":
            campaign_id = CampaignId.get(transaction, 7)
            url += f"cancelar/{campaign_id}"
            response = requests.put(url, headers=headers)
        else:
            return False

        if response.status_code == 200:
            return True
        else:
            return False

