import re
from enum import Enum
class BaseType(Enum):
    @classmethod
    def get_type(cls, t):
        properties = dir(cls)
        if not hasattr(cls, 'names'):
            for p in properties:
                if p.startswith('_'):
                    continue
                n = getattr(cls, p)
                v = n.value if type(t) == int else n
                if v == t:
                        return re.sub(r'\s|_', ' ', n.name)

class HasError(BaseType):
    Yes = 0
    No = 1