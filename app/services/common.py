

from uuid import UUID


def isValidUUID(value) -> bool:
    try:
        UUID(value)
 
        return True
    except ValueError:
        return False
    