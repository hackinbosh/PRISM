from enum import Enum

class Action(Enum):
    OBSERVE = "OBSERVE"
    ACTUATE = "ACTUATE"
    PARAMETERIZE = "PARAMETERIZE"
    CONFIGURE = "CONFIGURE"
    LINK = "LINK"
