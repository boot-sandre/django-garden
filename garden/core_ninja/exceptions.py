class GardenApplicationError(Exception):
    status_code = 405
    message = "CMS Garden: notify an error"

    def __init__(self, message, *args, **kwargs):
        if message:
            self.message = message

    def __str__(self):
        return repr(f"CMS Garden: {self.message}")
