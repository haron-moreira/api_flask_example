import re


class DateSchedule:

    @staticmethod
    def validate(date):
        pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z"
        if re.match(pattern, date):
            return True
        else:
            return False
