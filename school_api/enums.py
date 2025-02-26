from enum import Enum, IntEnum
# from enum import Enum


class LoggerTypes(IntEnum):
    DEBUG = 1
    ERROR = 2
    EXCEPTION = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
class ManagementRoles(IntEnum):
    ADMIN=1
    TEACHER=2
    STUDENT=3

class ResponseStatus(IntEnum):
    SUCCESS = 0
    ERROR = 1
    EXCEPTION = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]