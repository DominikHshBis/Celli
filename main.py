from abc import ABC, abstractmethod
from datetime import datetime
import traceback
import mein_test
#import inspect
import json
import os
import sys
import importlib
import random
import time
import inspect
import requests
import ast


class underground:

    

    def __init__(self, primary: mein_test.i_dataflow, secondary: mein_test.i_dataflow):
        
        self.primary = primary
        self.secondary = secondary

        self.active_pipe = primary
    
    def ask_ai_to_fix(self, pipe):

        module_file = inspect.getfile(
            pipe.__class__
        )

        current_source_file = (
            "generated_module.py"
        )

        if os.path.exists(
            current_source_file
        ):
            with open(
                current_source_file,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

        else:
            with open(
                module_file,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

        failed_source = pipe.get_failed_function_source(
            source
        )

        print(
            "===== FAILED FUNCTION ====="
        )

        print(
            failed_source
        )

        print(
            "===== END FAILED FUNCTION ====="
        )

        prompt = pipe.get_ai_prompt(
            source
        )

        response = requests.post(
            "https://ollama.hshbot.de/api/generate",
            json={
                "model": "deepseek-coder-v2:16b",
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        response.raise_for_status()

        generated_code = response.json()[
            "response"
        ]

        #
        # KI-Ausgabe bereinigen
        #
        generated_code = generated_code.strip()

        generated_code = generated_code.replace(
            "<code>",
            ""
        )

        generated_code = generated_code.replace(
            "</code>",
            ""
        )

        generated_code = generated_code.replace(
            "```python",
            ""
        )

        generated_code = generated_code.replace(
            "```",
            ""
        ).strip()

        print(
            "===== AI RESPONSE ====="
        )

        print(
            generated_code[:5000]
        )

        print(
            "===== END AI RESPONSE ====="
        )

        #
        # ERST JETZT Patch einsetzen
        #
        new_source = pipe.replace_failed_function(
            source,
            generated_code
        )

        with open(
            "last_ai_response.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                generated_code
            )

        with open(
            "generated_module.py",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                new_source
            )

        #
        # Gesamte Datei prüfen
        #
        try:

            compile(
                new_source,
                module_file,
                "exec"
            )

        except Exception as ex:

            print(
                "KI hat ungültigen Python-Code geliefert:"
            )

            print(
                ex
            )

            return False

        print(
            "Patch gespeichert:",
            os.path.abspath(
                "generated_module.py"
            )
        )

        return True

    def reload_pipe(self, pipe):

        module_name = pipe.__class__.__module__

        module = sys.modules[module_name]

        importlib.reload(module)

        new_class = getattr(
            module,
            pipe.__class__.__name__
        )
        print( "Reload Modul:", pipe.__class__.__module__)
        return new_class()

    def inject_error_into_module(
        self,
        pipe,
        errors
    ):

        module_file = inspect.getfile(
            pipe.__class__
        )

        with open(
            module_file,
            "r",
            encoding="utf-8"
        ) as f:

            source = f.read()

        class_name = pipe.__class__.__name__

        class_start = source.find(
            f"class {class_name}"
        )

        if class_start == -1:

            print(
                f"Klasse {class_name} nicht gefunden"
            )

            return False

        start_marker = "# ERROR_MEMORY_START"
        end_marker = "# ERROR_MEMORY_END"

        start = source.find(
            start_marker,
            class_start
        )

        end = source.find(
            end_marker,
            start
        )

        if start == -1 or end == -1:

            print(
                "ERROR_MEMORY Marker nicht gefunden"
            )

            return False

        if not isinstance(
            errors,
            list
        ):
            errors = [errors]


        error_text = repr(
            errors
        )
        #
        # Block neu erzeugen
        #
        #
# Block neu erzeugen
#
        #
# Block neu erzeugen

        error_text = repr(errors)

        error_text = error_text.replace(
            "\n",
            "\n        "
        )

        new_block = (
            "# ERROR_MEMORY_START\n"
            "        self.error_memory = "
            + error_text +
            "\n        # ERROR_MEMORY_END"
        )


        #
        # Zwischen den Markern ersetzen
        #
        source = (
            source[:start]
            + new_block
            + source[
                end + len(end_marker):
            ]
        )

        with open(
            module_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(source)

        print(
            f"{len(errors)} Fehler "
            f"in {module_file} integriert"
        )

        return True

    def recover_pipe(self, pipe):

        print(
            f"Recovery startet "
            f"{pipe.pipe_id}"
        )

        pipe.status = "recovering"

        tmp_file = f"{pipe.pipe_id}.tmp"

        if not os.path.exists(tmp_file):

            print(
                "Keine Fehlerdatei"
            )

            return

        with open(
            tmp_file,
            "r",
            encoding="utf-8"
        ) as f:

            errors = json.load(f)

        success = self.inject_error_into_module(
            pipe,
            errors
        )

        if not success:

            return

        os.remove(
            tmp_file
        )

        print(
            "Fehler in Modul integriert"
        )

        print(
            "KI erhält aktualisierten "
            "Klassenquelltext"
        )

        success = self.ask_ai_to_fix(
            pipe
        )

        if not success:

            print(
                "KI-Reparatur fehlgeschlagen"
            )

            return

        new_pipe = self.reload_pipe(
            pipe
        )

        new_pipe.status = "online"

        if pipe == self.primary:

            self.primary = new_pipe

        else:

            self.secondary = new_pipe

        if self.active_pipe == pipe:

            self.active_pipe = new_pipe

        print(
            f"{new_pipe.pipe_id} "
            f"neu geladen"
        )


    def switch_pipe(self):

        if self.active_pipe == self.primary:

            target = self.secondary

        else:

            target = self.primary

        if target.status == "online":

            print(
                f"FAILOVER: "
                f"{self.active_pipe.pipe_id}"
                f" -> "
                f"{target.pipe_id}"
            )

            self.active_pipe = target

            return True

        return False
def main():

    p1 = mein_test.datapipe_1()
    p2 = mein_test.datapipe_2()

    ug = underground(
        primary=p1,
        secondary=p2
    )

    while True:

        pipe = ug.active_pipe

        func = random.choice([
            pipe.test1,
            pipe.test2,
            pipe.test3
        ])

        try:

            print(
                "\nAktive Pipe:",
                pipe.pipe_id,
                func.__name__
            )

            func()

        except Exception as ex:

            print(
                f"Fehler in {pipe.pipe_id}:",
                ex
            )

            old_pipe = pipe

            switched = ug.switch_pipe()

            if switched:

                print(
                    "Ersatzpipeline übernommen"
                )

                ug.recover_pipe(old_pipe)

            else:

                print(
                    "Beide Pipelines offline"
                )

        time.sleep(4)

# class underground():
#     def __init__(self,i_dataflow:i_dataflow = None):
#         if i_dataflow is None:
#             raise ValueError("keine i_dataflow Instanz übergeben")
#         self.i_dataflow: i_dataflow = i_dataflow
    
main()