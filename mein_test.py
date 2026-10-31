from abc import ABC, abstractmethod
from datetime import datetime
import traceback
#import inspect
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
        self.ki_guidlines = "passe nur die funktionen so an dass sie aufgrundlage der in error_memory enthaltenen Fehler die Funktionen absicherst und auch nur dort wo der Fehler aufgetreten ist. verändere nichts anderes innerhalb dieser klasse. schreibe im anschluss den passenden Test dazu in dieses Modul"

    

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

        #
        # Fehler an error_memory anhängen
        #
        self.error_memory.append(error)

        #
        # Kompletten Speicherstand schreiben
        #
        with open(
            f"{self.pipe_id}.tmp",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.error_memory,
                f,
                indent=4
            )

        self.status = "offline"
    

    def track_errors(func):
        @wraps(func)
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

    pipe_id = "pipe_001"

    def __init__(self):

        super().__init__()

        # ERROR_MEMORY_START
        self.error_memory = [{'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:17:44.851928', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 116, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:18:43.302766', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 116, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:18:59.313181', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 116, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:19:11.321363', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 116, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:19:27.332741', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 116, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:22:59.337034', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 117, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:23:27.347385', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 117, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:23:35.356334', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 117, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T14:24:03.368674', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 117, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}]
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
        self.error_memory = [{'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:17:52.856093', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 137, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:18:47.306879', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 137, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:19:07.317461', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 137, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:19:23.328150', 'line': 72, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 72, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 137, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:23:03.342063', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 138, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:23:31.351718', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 138, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:23:39.360886', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 138, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T14:24:31.379104', 'line': 73, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 73, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 138, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}]
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





        


