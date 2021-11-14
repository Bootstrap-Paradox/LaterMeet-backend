
class Error(Exception):
    pass


class NotFound(Error):
    def __init__(self, message: str = "Not Found") -> None:
        self.message = message
        super(NotFound, self).__init__(self.message)

    def __str__(self) -> str:
        return self.message


class NotAllowed(Error):
    def __init__(self, message: str = "Not Allowed") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class Restricted(Error):
    def __init__(self, message: str = "Restricted") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class Expired(Error):
    def __init__(self, message: str = "Expired") -> None:
        self.message = message

    def __str__(self):
        return self.message
