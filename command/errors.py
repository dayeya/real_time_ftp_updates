
class CommandError(AttributeError):
    """
    CommandError indicates that a non-existent command was used.
    """
    def __init__(self, *args: object, name: str | None = ..., obj: object = ...) -> None:
        super().__init__(*args, name=name, obj=obj)