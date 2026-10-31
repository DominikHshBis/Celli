from abc import ABC, abstractmethod
from datetime import datetime
import traceback
import json
import re
import os
import sys
import importlib
import random
import time
from functools import wraps

class i_dataflow(ABC):
    pipe_id = "pipe_001"
    version = "0"
    
    def __init__(self):
        self.error_memory = []       
        self.status= "online"
        self.ki_guidlines = "in self.error_memory sind alle bisher aufgetretenen Fehler dieser Klasse, löse den Fehler in den in self.error_memory enthaltenen funktionen (pfad wird dort angegeben) innerhalb der logik, so dass der fehler nicht mehr auftreten kann "

    def get_ai_prompt(self, source):

        last_error = (
        self.error_memory[-1]
        if self.error_memory
        else "Kein Fehler vorhanden"
        )
        return f"""


        {self.ki_guidlines}

        WICHTIG:

        Die Marker

        # ERROR_MEMORY_START
        # ERROR_MEMORY_END

        dürfen niemals entfernt,
        verschoben oder verändert werden.

        LETZTER FEHLER:

        {self.error_memory[-1]}

        AKTUELLER CODE:

        {source}
        """


    def track_error(self, func_name, exc):
        error = {
            "pipe_id": self.pipe_id,
            "version": self.version,
            "class_name": self.__class__.__name__,
            "module": self.__class__.__module__,
            "function": func_name,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "line": exc.__traceback__.tb_lineno,
            "traceback": traceback.format_exc()
        }
        self.error_memory.append(error)
        with open(f"{self.pipe_id}.tmp", "w", encoding="utf-8") as f:
            json.dump(self.error_memory, f, indent=4)
        self.status = "offline"
    
    def track_errors(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as ex:
                self.track_error(func.__name__, ex)
                raise
        return wrapper
    
    @abstractmethod
    def test1(self):
        pass
    @abstractmethod
    def test2(self):
        pass
    @abstractmethod
    def test3(self):
        pass

class datapipe_1(i_dataflow):
    pipe_id = "pipe_001"
    def __init__(self):
            
        super().__init__()
        # ERROR_MEMORY_START
        self.error_memory = []
        # ERROR_MEMORY_END
    
    @i_dataflow.track_errors
    def test1(self):
        print("pipe1:", "test1")

    @i_dataflow.track_errors
    def test2(self):
        print("pipe1:", "test2")

    @i_dataflow.track_errors
    def test3(self):
        raise ValueError("TEST3_ERROR")
        
class datapipe_2(i_dataflow):
    pipe_id = "pipe_002"
    def __init__(self):
        super().__init__()
        # ERROR_MEMORY_START
        self.error_memory = []
        # ERROR_MEMORY_END
    @i_dataflow.track_errors
    def test1(self):
        print("pipe2:","test1")

    @i_dataflow.track_errors
    def test2(self):
        print("pipe2:","test2")
        raise ValueError("TEST2_ERROR")
    
    @i_dataflow.track_errors
    def test3(self):
        print("pipe2:","test3")