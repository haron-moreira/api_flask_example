class Spliter:

    @staticmethod
    def spliter_token(headers):

        if "Authorization" in headers:
            partes = headers["Authorization"].split()
            if len(partes) == 2 and partes[0].lower() == "bearer":
                return partes[1]
        else:
            return None
