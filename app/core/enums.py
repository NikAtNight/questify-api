from enum import Enum


class BaseEnum(Enum):
    """Base enum prototype.

    Enforces value uniqueness and meaningful string transformation."""

    def __init__(self, *args):
        cls = self.__class__
        if any(self.value == e.value for e in cls):
            a = self.name
            e = cls(self.value).name
            raise ValueError(
                'duplicates not allowed:  {} --> {}'.format(a, e)
            )

    def __str__(self):
        return self.value

    @classmethod
    def keys(cls):
        items = cls.__members__.items()
        key_list = [e[0] for e in items]

        return key_list

    @classmethod
    def values(cls):
        value_list = [e.value for e in cls]

        return value_list

    @classmethod
    def tuples(cls):
        items = cls.__members__.items()
        for k, v in items:
            pass

        tuple_list = [(k, str(v)) for k, v in items]

        return tuple_list

    @classmethod
    def includes(cls, value):
        try:
            cls(value)
            return True
        except Exception:
            return False


class DifficultyLevelEnum(BaseEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class HabitStatusEnum(BaseEnum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ABANDONED = "Abandoned"
