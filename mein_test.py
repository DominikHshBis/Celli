from abc import ABC, abstractmethod
from datetime import datetime
import traceback
#import inspect
import json

class i_dataflow(ABC):
    NODE_ID = "pipe_001"

    def __init__(self):
        self.error_memory = {}

    def track_error(self, func_name, exc):

        error = {
        "node_id": self.NODE_ID,
        "class_name": self.__class__.__name__,
        "module": self.__class__.__module__,
        "function": func_name,
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "timestamp": datetime.utcnow().isoformat(),

        # Zeile im Code
        "line": exc.__traceback__.tb_lineno,

        # kompletter Traceback
        "traceback": traceback.format_exc()
    }
        with open("errors.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(error))
            f.write("\n")
            
    def track_errors(func):

        def wrapper(self, *args, **kwargs):

            try:
                return func(self, *args, **kwargs)

            except Exception as ex:

                self.track_error(
                    func.__name__,
                    ex
                )

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
    @i_dataflow.track_errors
    def test1(self):
        print("pipe1:","test1")

    @i_dataflow.track_errors
    def test2(self):
        print("pipe1:","test2")
    
    @i_dataflow.track_errors
    def test3(self):
        raise ValueError("TEST3_ERROR")
        

class datapipe_2(i_dataflow):

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


class underground():
    def __init__(self,i_dataflow:i_dataflow = None):
        if i_dataflow is None:
            raise ValueError("keine i_dataflow Instanz übergeben")
        self.i_dataflow: i_dataflow = i_dataflow
    
p1 = datapipe_1()
p2 = datapipe_2()

ug =underground(p1)


ug.i_dataflow.test3()



