class QueueErr(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class QueueEmptyException(QueueErr):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class QueueFullException(QueueErr):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
