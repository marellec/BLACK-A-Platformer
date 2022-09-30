
# mixin that adds on/off functionality to a Trait (or another class)
class Toggleable():
    
    @property
    def able(self) -> bool: return self._able
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._able = True
    
    def disable(self): self._able = False
    def enable(self):  self._able = True