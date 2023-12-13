from datetime import datetime


class ValidaData:

    @staticmethod
    def range_of_date(dt_inicio, dt_final):
        dt_inicio = datetime.strptime(dt_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt_final = datetime.strptime(dt_final, "%Y-%m-%dT%H:%M:%S.%fZ")

        if dt_inicio >= dt_final:
            return False

        return True
