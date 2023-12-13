class Fail:

    @staticmethod
    def fail(erro, transaction='0'):
        erros_mapeados = {
            "405": {
                'error': 'method not allowed, change the HTTP method and try again',
                'code': 405
            },
            "500": {
                "error": "server error, application failure",
                "code": 500
            },
            "404": {
                "error": "resource not found",
                "code": 404
            },
            "400-1": {
                "error": "bad request, review your body data and try again",
                "code": 400
            },
            "401-1": {
                "error": "unauthorized, review your body data or authorization and try again",
                "code": 401
            },
            "400-2": {
                "error": "command not supported, please, insert a valid command and try again",
                "code": 400
            },
            "400-3": {
                "error": "bad request, maybe campaign status can't be changed or has changed before",
                "code": 400
            },
            "400-4": {
                "error": "bad request, start date or end date are invalid",
                "code": 400
            },
            "403-1": {
                "error": "unauthorized, if you think this a mistake, let us know.",
                "code": 403
            },
            "415": {
                "error": "unsupported media type, the content-type should be application/json",
                "code": 415
            }
        }

        if erro in erros_mapeados:
            return erros_mapeados[erro]

        return {"error": "unknown error", "code": 501}
