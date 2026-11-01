from abc import ABCMeta, ABC, abstractmethod
from datetime import datetime
import traceback
import json

from functools import wraps
import ast

class Auto_Track_Meta(ABCMeta):

    def __new__(cls, name, bases, attrs):

        if name == "i_dataflow":
            return super().__new__(
                cls,
                name,
                bases,
                attrs
            )

        base_methods = set()

        for base in bases:
            base_methods.update(
                base.__dict__.keys()
            )

        new_cls = super().__new__(
            cls,
            name,
            bases,
            attrs
        )

        for key, value in attrs.items():

            if (
                callable(value)
                and not key.startswith("_")
                and key not in base_methods
            ):

                setattr(
                    new_cls,
                    key,
                    new_cls.track_errors(
                        value
                    )
                )

        return new_cls
class i_dataflow(ABC,metaclass=Auto_Track_Meta):

    pipe_id = ""
    version = "0"
    
    def __init__(self):
        self.error_memory = []       
        self.status= "online"
        self.ki_guidlines = "in self.error_memory sind alle bisher aufgetretenen Fehler dieser Klasse, löse den Fehler in den in self.error_memory enthaltenen funktionen (pfad wird dort angegeben) innerhalb der logik, so dass der fehler nicht mehr auftreten kann."

    def get_ai_prompt(self, source):

    
        failed_source = self.get_failed_function_source(
            source
        )

        open_errors = self.get_open_errors()

        last_error = (
            open_errors[-1]
            if open_errors
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

        original_line = lines[
            info["start"] - 1
        ]

        indent = len(
            original_line
        ) - len(
            original_line.lstrip()
        )

        patch_lines = [
            (" " * indent) + line
            if line.strip()
            else ""
            for line in patch_code.splitlines()
        ]

        new_lines = (
            lines[:info["start"] - 1]
            + patch_lines
            + lines[info["end"]:]
        )

        return "\n".join(
            new_lines
    )

    def get_failed_function(self, source):

        open_errors = self.get_open_errors()

        if not open_errors:
            return None

        func_name = open_errors[-1]["function"]

        class_name = self.__class__.__name__

        tree = ast.parse(source)

        for node in tree.body:

            if (
                isinstance(node, ast.ClassDef)
                and node.name == class_name
            ):

                for item in node.body:

                    if (
                        isinstance(
                            item,
                            ast.FunctionDef
                        )
                        and item.name == func_name
                    ):

                        return {
                            "name": item.name,
                            "start": item.lineno,
                            "end": item.end_lineno
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
            "traceback": traceback.format_exc(),
            "status": "open",
            "fixed_at": None
    

        }
        self.error_memory.append(error)
        with open(f"{self.pipe_id}.tmp", "w", encoding="utf-8") as f:
            json.dump(self.error_memory, f, indent=4)
        self.status = "offline"
    
    def get_open_errors(self):

        return [
            error
            for error in self.error_memory
                if error.get(
                    "status",
                    "open"
                ) == "open"
            ]

    def mark_last_error_fixed(self):

        open_errors = self.get_open_errors()

        if open_errors:

            open_errors[-1]["status"] = "fixed"

            open_errors[-1]["fixed_at"] = (
                datetime.utcnow().isoformat()
        )

    def track_errors(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):

            print("CALL:", func.__name__)

            try:

                result = func(self, *args, **kwargs)

                print(
                    "OK:",
                    func.__name__
                )

                return result

            except Exception as ex:

                print(
                    "EXCEPTION:",
                    func.__name__,
                    ex
                )
                self.track_error(
                    func.__name__,
                    ex
                )
                raise
        return wrapper
    
    # @abstractmethod
    # def test1(self):
    #     pass
    # @abstractmethod
    # def test2(self):
    #     pass
    # @abstractmethod
    # def test3(self):
    #     pass

class datapipe_1(i_dataflow):
    pipe_id = "pipe_001"
    def __init__(self):
            
        super().__init__()
        # ERROR_MEMORY_START
        self.error_memory = []
        # ERROR_MEMORY_END
    
    def test1(self):
        print("pipe1:", "test1")
    
    def test2(self):
        print("pipe1:", "test2")
    
    def test3(self):
        raise ValueError("TEST3_ERROR")
        
class datapipe_2(i_dataflow):
    pipe_id = "pipe_002"
    def __init__(self):
        super().__init__()
        # ERROR_MEMORY_START
        self.error_memory = []
        # ERROR_MEMORY_END
   
    def test1(self):
        print("pipe2:","test1")

    def test2(self):
        print("pipe2:","test2")
        raise ValueError("TEST2_ERROR")
    
    def test3(self):
        print("pipe2:","test3")