class Success:

    @staticmethod
    def success_return(status, transaction='0', token='0', expiration_time="0", body_main=0, details=0, action="",
                       start_date="", end_date="", information_json=""):
        retornos = {
            "200-1": {
                'description': 'login completed with success',
                'code': 200,
                'token': token,
                'token_duration': expiration_time
            },
            "200-2": {
                'description': f'messages on queue, check the status on /WaveMessage/api/v1/message/{transaction}',
                'code': 201,
                'transaction': transaction
            },
            "200-3": {
                'description': f'details of your sms campaign',
                'code': 200,
                "main_information": body_main,
                "phone_information": details
            },
            "200-4": {
                'description': f'command accepted, changes applied',
                'code': 200,
                "action_executed": action,
                "transaction": transaction
            },
            "200-5": {
                'description': f'search completed',
                'code': 200,
                "dates": {
                    "start_date": start_date,
                    "end_date": end_date},
                "information": information_json
            },

        }

        if status in retornos:
            return retornos[status]

        return {"success": "request ok", "code": 202}
