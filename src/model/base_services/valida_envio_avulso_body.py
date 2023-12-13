class ValidaBodyEnvioAvulso:

    @staticmethod
    def valida(body):

        if len(body) < 4:
            return False

        params_accepted = ['schedule',
                           'quantity', 'cost_center', 'details',
                           'message', 'name', 'product_id',
                           'phones', 'urlCallbackSend', 'urlCallbackAnswer', 'shortlyUrl',
                           'whatsappId', 'tags', 'auto_answer', 'blockListId'
                           ]

        for param in body:
            if param not in params_accepted:
                return False

        if "phones" not in body or "name" not in body or "message" not in body:
            return False

        if len(body["phones"].split(" ")) > 100:
            return False

        return True
