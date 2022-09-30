
from dataclasses import dataclass
from typing import Callable, Sequence
from base_labels import Label
from controls import ControlInput, Controller




class Combo:
    
    label: Label
    
    sequence: tuple[Label, ...]
    excepted_keys: tuple[Label, ...]
    
    # min_hold_times: tuple[int, ...]
    max_hold_times: tuple[int, ...]
    
    max_space_times: tuple[int, ...]
    
    perform_funct: Callable
    cancel_funct: Callable
    
    flow: list[Label]

    @property 
    def key_name(self) -> Label: return self.sequence[self._i]
    
    # @property 
    # def min_hold_time(self) -> int: return self.min_hold_times[self._i]
    @property 
    def max_hold_time(self) -> int: return self.max_hold_times[self._i - 1]
    
    # @property 
    # def min_space_time(self) -> int: return self.min_space_times[self._i - 1]
    @property 
    def max_space_time(self) -> int: return self.max_space_times[self._i - 1]
    
    @property # just pressed the next key in sequence
    def progressed(self) -> bool: return self._progressed > 0
    
    
    def __init__(self, 
                 label,
                 keys: Sequence[Label],
                 perform_funct: Callable,
                 cancel_funct: Callable = lambda *args, **kwargs : None,
                 *,
                 excepted_keys: Sequence[Label] = tuple(),
                 #  min_hold_time: int = 0,
                 max_hold_time: int = 5,
                 max_space_time: int = 5,
                 #  min_hold_times: Sequence[int] = tuple(),
                 max_hold_times: Sequence[int] = tuple(),
                 max_space_times: Sequence[int] = tuple()):
        self.label = Label(label.name + " combo")
        
        self.sequence = tuple(k for k in keys)
        self.excepted_keys = tuple(k for k in excepted_keys)
        
        # if (min_hold_times == tuple()):
        #     self.min_hold_times = tuple(min_hold_time for _ in (range(len(self) - 1)))
        # else:
        #     self.min_hold_times = tuple(m for m in min_hold_times)
        
        if (max_hold_times == tuple()):
            self.max_hold_times = tuple(max_hold_time for _ in (range(len(self))))
        else:
            self.max_hold_times = tuple(m for m in max_hold_times)
        
        if (max_space_times == tuple()):
            self.max_space_times = tuple(max_space_time for _ in (range(len(self) - 1)))
        else:
            self.max_space_times = tuple(s for s in max_space_times)
            
        self.perform_funct = perform_funct # type: ignore
        self.cancel_funct = cancel_funct   # type: ignore
        
        self._progressed = 0
        
        self._i = 0
        
        self._space_time = 0
        self.flow = []
        
        print()
        print(f"{self.label = }")
        print(f"{self.sequence = }")
        print(f"{self.excepted_keys = }")
        print(f"{self.max_hold_times = }")
        print(f"{self.max_space_times = }")
    
    
    def respond_to_input(self,
                         *args,
                         controller: Controller,
                         dt: int,
                         **kwargs):
        
        self._space_time += 1
        
        # if ongoing combo,
        # check non-excepted wrong keys to see if they broke the combo
        # stop checking if combo broken
        for key in controller.keys.values():
            
            if (key.label != self.key_name and
                key.label not in self.excepted_keys and
                key.get_state(ControlInput.PRESSED)):
                print(f"{key.label} intercepted >[")
                self.cancel()
                return
        
        # check previous keys to see if they've timed out
        # stop checking if combo broken
        for key_name, max_hold_time in zip(self.flow, 
                                           self.max_hold_times):
            
            # over time
            if (controller.get_down(key_name) > max_hold_time):
                print(f"{key_name} held overtime :[")
                self.cancel()
                return
            
            # under time
            # if (controller.get_key_state(self.key_name, ControlInput.RELEASED)):
            #     pass
        
        
        # check if next key timed out (over time)
        if (0 < len(self.flow) < len(self.sequence) and # actually started and before last key
            self._space_time > self.max_space_time):
            
            print(f"{self.key_name} spaced overtime :O")
            self.cancel()
            return
        
        self._progressed -= 1
        
        # check if next key has been pressed in time
        if (controller.get_key_state(self.key_name, ControlInput.PRESSED)):
            # check under time (min_space_time)
            
            self.flow.append(self.key_name)
            
            print(f"{self.key_name}...")
            
            self._progressed = 2
            
            self._i += 1
            if (self._i < len(self.sequence)):
                self._space_time = 0
            else:
                self._i = len(self.sequence) - 1
        
            
        
        
        # almost finished the move...
        if (len(self.flow) == len(self.sequence) and
            controller.get_key_state(self.key_name, ControlInput.RELEASED)):
                
            # check over time (max_hold_time)
            if (controller.get_prev_down(self.key_name) > self.max_hold_time):
                print(f"{self.key_name} held overtime :[")
                self.cancel()
                return
        
            # check under time (min_hold_time)

            
            
            # call trait's perform funct
            self.perform_funct(*args, dt=dt, **kwargs)
            
            # print(f"{self._i = }, {self._space_time = }, {self.flow = }")
            self.reset()
    
    
    def cancel(self): 
        if (len(self.flow) > 0): # actually started
            # reset time records
            self.reset()
            # call trait's cancel funct
            self.cancel_funct()
        # print(f"{self._i = }, {self._space_time = }, {self.flow = }")
        
    def reset(self): 
        # reset time records
        self._i = 0
        
        self._space_time = 0
        self.flow = []
        self._progressed = 0
    
    def __len__(self):
        return len(self.sequence)






class Combo1Key:
    
    key_name: Label
    
    @property
    def can_perform(self) -> bool: return (self.ready == 1)
    
    @can_perform.setter
    def can_perform(self, val: bool): 
        if (val): self.ready = 1
        else: self.ready -= 1 # delay returning True for confirmed performing by 1 frame
        
    # STILL UNSURE HOW IT WORKS
    @property # delay returning True for confirmed performing by 1 frame
    def confirmed_performing(self) -> bool: return (self.performing and self.ready < 0)
    
    
    @property # delay confirming True for confirmed performing by 1 frame
    def confirmed(self) -> bool: return (self.ready == -1)
    
    # STILL UNSURE HOW IT WORKS
    @property # delay returning True for confirmed performing by 1 frame
    def performing(self) -> bool: return (self._engage_time < self._max_time)
    
    
    @property
    def engage_time(self) -> int: return self._engage_time
    @property
    def max_time(self) -> int: return self._max_time
    
    @property
    def request_time(self) -> int: return self._request_time
    @property
    def accept_time(self) -> int: return self._accept_time
    
    perform_funct: Callable
    cancel_funct: Callable
    
    def __init__(self,
                 key_name: Label,
                 max_time: int,
                 accept_time: int,
                 perform_funct: Callable,
                 cancel_funct: Callable = lambda *args, **kwargs : None):
        self.key_name = key_name
        
        self.ready = 0
        
        self._engage_time = max_time
        self._max_time = max_time
        
        self._request_time = 0
        self._accept_time = accept_time
        
        self.perform_funct = perform_funct # type: ignore
        self.cancel_funct = cancel_funct   # type: ignore
        
    
    def respond_to_input(self,
                         *args,
                         controller: Controller,
                         dt: int,
                         **kwargs):
        
        if (controller.get_key_state(self.key_name, ControlInput.PRESSED)):
            self.begin()
        if (controller.get_key_state(self.key_name, ControlInput.RELEASED)):
            self.cancel()
            
        if (self._request_time > 0): # asked to begin performing,
                                     # still in accepting window
            
            if (self.can_perform): # can perform
                self._engage_time = 0 # start performing
                self._request_time = 0 # close request
                
                # self.grounded = False # (if started_performing)
            
            self._request_time -= dt # decrement request time
        
        if (self.performing): # performing, but not 
                              # necessarily confirmed
            # call trait's perform funct
            self.perform_funct(*args, dt=dt, **kwargs)
            
            self._engage_time += dt # increment engage time
            
        self.can_perform = False # whether performing or not, 
                                 # reset ability to perform
            
            
    def begin(self):
        # set time request record (ask to begin performing)
        self._request_time = self._accept_time
        
    def cancel(self): 
        # reset time records
        self._engage_time = self._max_time
        self._request_time = 0
        # call trait's cancel funct
        self.cancel_funct()
        
    
        