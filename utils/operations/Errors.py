
class Error(Exception):
    pass


class NotFound(Error):
    def __init__(self, message: str = "Not Found") -> None:
        self.message = message
        super(NotFound, self).__init__(self.message)

    def __str__(self):
        return self.message
