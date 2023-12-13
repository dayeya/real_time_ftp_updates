
class SocketConnectionError(ConnectionRefusedError):
    """
    SocketConnectionError indicates that a connection was made over a closed machine.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)