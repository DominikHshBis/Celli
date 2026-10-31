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
import ast

class i_dataflow(ABC):
    pipe_id = "pipe_001"
    version = "0"
    
    def __init__(self):
        self.error_memory = []       
        self.status= "online"
        self.ki_guidlines = "in self.error_memory sind alle bisher aufgetretenen Fehler dieser Klasse, löse den Fehler in den in self.error_memory enthaltenen funktionen (pfad wird dort angegeben) innerhalb der logik, so dass der fehler nicht mehr auftreten kann."

    def get_ai_prompt(self, source):

    
        failed_source = self.get_failed_function_source(
            source
        )

        last_error = (
            self.error_memory[-1]
            if self.error_memory
            else "Kein Fehler vorhanden"
        )

        return f"""
            {self.ki_guidlines}

            FEHLERHAFTE FUNKTION:

            {failed_source}

            LETZTER FEHLER:

            {last_error}

            Gib ausschließlich die korrigierte Funktion zurück.

            Keine Erklärungen.
            Kein Markdown.
            Keine Kommentare.
            Keinen weiteren Code.

            WICHTIG:

            Die Funktion ist fehlerhaft.

            error_memory darf nicht verändert werden.

            track_error darf nicht aufgerufen werden.

            Der Decorator

            @i_dataflow.track_errors

            übernimmt das Fehlerhandling bereits.

            Die Funktion darf keine Einträge in error_memory schreiben.

            Die Funktion darf den Fehler nicht erneut werfen.

            Eine Reparatur muss dazu führen,
            dass die Funktion erfolgreich beendet wird.

            """


        # last_error = (
        # self.error_memory[-1]
        # if self.error_memory
        # else "Kein Fehler vorhanden"
        # )
        # return f"""


        # {self.ki_guidlines}

        # WICHTIG:  
        
        # Die Marker
        
        # # ERROR_MEMORY_START
        # # ERROR_MEMORY_END

        # dürfen niemals entfernt,
        # verschoben oder verändert werden.

        # nichts erklären,  gib bitte nur den code zurück

        # Antworte ausschließlich im Format:

        # <code>
        # ...
        # </code>

        # Kein Text vor <code>.
        # Kein Text nach </code>.

        # Der Fehler darf nicht lediglich unterdrückt werden.

        # Die Ursache des Fehlers ist zu beheben.

        # try/except Blöcke dürfen nur eingesetzt werden,
        # wenn sie die Ursache tatsächlich beseitigen.

        # Das bloße Abfangen einer Exception gilt nicht als Reparatur.

        # Du darfst keinen Code außerhalb vorhandener Klassen schreiben.

        # Du darfst keinen Code außerhalb vorhandener Funktionen schreiben.

        # Verändere ausschließlich die Funktion, die den Fehler verursacht hat.

        # last_error = self.error_memory[-1]

        # LETZTER FEHLER:

        # Funktion:
        # {last_error['function']}

        # Typ:
        # {last_error['error_type']}

        # Meldung:
        # {last_error['error_message']}

        # Traceback:
        # {last_error['traceback']}

        # Die genannte Funktion verursacht aktuell den Fehler.

        # Ändere die Logik dieser Funktion so,
        # dass dieser Fehler nicht mehr auftreten kann.

        # Gib ausschließlich Python-Code zurück.

        # Gib ausschließlich die korrigierte Funktion zurück.

        # Beispiel:

        # def test3(self):
        #     ...

        # Keinen weiteren Code.
        # Keine Klassen.
        # Keine Erklärungen.
        
        # """


    def replace_failed_function(
        self,
        source,
        patch_code
    ):

        info = self.get_failed_function(
            source
        )

        if not info:
            return source

        lines = source.splitlines()

        patch_lines = patch_code.splitlines()

        new_lines = (
            lines[:info["start"] - 1]
            + patch_lines
            + lines[info["end"]:]
        )

        return "\n".join(
            new_lines
    )

    def get_failed_function(self, source):

        if not self.error_memory:
            return None

        func_name = self.error_memory[-1][
            "function"
        ]

        tree = ast.parse(source)

        for node in ast.walk(tree):

            if (
                isinstance(
                    node,
                    ast.FunctionDef
                )
                and node.name == func_name
            ):

                return {
                    "name": node.name,
                    "start": node.lineno,
                    "end": node.end_lineno
                }

        return None

    def get_failed_function_source(
        self,
        source
        ):
        info = self.get_failed_function(
            source
        )

        if not info:
            return None

        lines = source.splitlines()

        return "\n".join(
            lines[
                info["start"]-1:
                info["end"]
            ]
        )

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
        self.error_memory = [{'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:35:04.078807', 'line': 76, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 76, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 111, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:45:42.667883', 'line': 97, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 97, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 132, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:50:42.602997', 'line': 95, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 95, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 130, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:51:45.919000', 'line': 95, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 95, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 130, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:54:33.715624', 'line': 106, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 106, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 141, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:57:21.550933', 'line': 108, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 108, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 143, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T15:58:25.432391', 'line': 108, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 108, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 143, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:10:30.637481', 'line': 119, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 119, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 154, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:11:19.661840', 'line': 119, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 119, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 154, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:32:27.504591', 'line': 213, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 213, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 248, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:33:01.530651', 'line': 213, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 213, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 248, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:33:11.465215', 'line': 213, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 213, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 248, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:41:13.775038', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:43:53.302939', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:44:31.283727', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:45:05.133227', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:45:50.933036', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:46:02.507491', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 247, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:48:26.724593', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:49:40.314441', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:53:19.424159', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:53:53.774862', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:54:53.843528', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:55:43.016659', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:56:35.518176', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:56:59.172516', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:57:53.978528', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:58:11.943093', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-10-31T16:58:52.171016', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 269, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n'}]
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
        self.error_memory = [{'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:10:46.894451', 'line': 119, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 119, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 170, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:32:56.546846', 'line': 213, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 213, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 264, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:33:06.579922', 'line': 213, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 213, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 264, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:41:25.466948', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 263, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:44:14.965466', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 263, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:45:22.110520', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 263, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:45:56.105451', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 263, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:46:10.222742', 'line': 212, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 212, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 263, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:49:18.493502', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:53:32.928440', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:54:16.406791', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:55:17.602072', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:56:16.451421', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:56:44.947128', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:57:25.528233', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:57:59.401487', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:58:38.819026', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-10-31T16:59:00.645205', 'line': 234, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 234, in wrapper\n    return func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 285, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n'}]
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