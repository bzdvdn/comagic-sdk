class ComagicException(Exception):
    def __init__(self, error_data, *args, **kwargs):
        self.error_data = error_data
        super().__init__(args, kwargs)

    def __str__(self):
        return f"Code: {self.error_data['code']}, message: {self.error_data['message']}, data: " \
               f"{self.error_data.get('data')}"


class ComagicParamsError(Exception):
    def __init__(self, error_message: str, *args, **kwargs):
        self.error_message = error_message
        super().__init__(args, kwargs)

    def __str__(self):
        return self.error_message
