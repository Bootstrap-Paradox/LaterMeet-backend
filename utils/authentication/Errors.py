

class Error(Exception):
    pass


class AuthenticationError(Error):
    def __init__(self, message="There was An Internal Error while Authentication") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class UserAlreadyExistError(Error):
    def __init__(self, authentication_data, message="User with Provided data Already Exists") -> None:
        self.authentication_data = authentication_data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class UserNotFound(Error):
    def __init__(self, email="", message=None) -> None:
        self.email = email
        self.message = message if isinstance(
            message, str) else f"User with {self.email} does not Exist in the Database "
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
