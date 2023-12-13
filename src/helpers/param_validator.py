class Params:

    @staticmethod
    def validate(param):
        params_type = ("start", "pause", "cancel")

        if param not in params_type:
            return False

        return True
