class PathNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CommandNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
