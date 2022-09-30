from dataclasses import dataclass, field


# make a new label ID 
def create_Label_ID(name: str) -> int:
    return int("".join(str(ord(ch)) for ch in name))

# for use in Trait dictionary as a Trait identifier
@dataclass(frozen=True)
class Label:
    name: str = field(compare=False)
    ID: int = field(init=False)
    
    def __init__(self, name: str):
        super().__setattr__('name', name)
        super().__setattr__('ID', create_Label_ID(name))
        
    def __str__(self) -> str:
        return f"Label({self.name})"
    
    def __repr__(self) -> str:
        return str(self)
        

class DirLabel(Label):

    options: dict[str, str] = { 
        "up"     : "DIR_UP", 
        "down"   : "DIR_DOWN", 
        "left"   : "DIR_LEFT", 
        "right"  : "DIR_RIGHT",
        "None"   : "DIR_NONE"
    }
    
    def __init__(self, name: str):
        if (name not in DirLabel.options):
            raise ValueError(f"DirLabel name must be one of {DirLabel.options}")
        
        super().__init__(name)
        
    def __str__(self) -> str:
        return self.options[self.name]


class SideLabel(Label):

    options: dict[str, str] = { 
        "top"    : "TOP_SIDE", 
        "bottom" : "BOTTOM_SIDE", 
        "left"   : "LEFT_SIDE", 
        "right"  : "RIGHT_SIDE",
        "None"   : "NONE_SIDE"
    }
    
    def __init__(self, name: str):
        if (name not in SideLabel.options):
            raise ValueError(f"SideLabel name must be one of {SideLabel.options}")
        
        super().__init__(name)
        
    def __str__(self) -> str:
        return self.options[self.name]
    
    
DIR_UP = DirLabel("up")
DIR_DOWN = DirLabel("down")
DIR_LEFT = DirLabel("left")
DIR_RIGHT = DirLabel("right")

DIR_NONE = DirLabel("None")

TOP_SIDE = SideLabel("top")
BOTTOM_SIDE = SideLabel("bottom")
LEFT_SIDE = SideLabel("left")
RIGHT_SIDE = SideLabel("right")

NONE_SIDE = SideLabel("None")