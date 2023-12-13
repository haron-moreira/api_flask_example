class ValidaBodyLogin:

    @staticmethod
    def valida(body):
        if "username" not in body or "password" not in body:
            return False

        if len(body) != 2:
            return False

        return True
