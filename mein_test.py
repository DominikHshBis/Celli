from healer import i_dataflow

class datapipe_1(i_dataflow):
    pipe_id = "pipe_001"
    def __init__(self):
            
        super().__init__()
        # ERROR_MEMORY_START
        self.error_memory = [{'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-11-01T21:02:01.086010', 'line': 291, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 291, in wrapper\n    result = func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 332, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n', 'status': 'fixed', 'fixed_at': '2026-11-01T21:02:01.087594'}, {'pipe_id': 'pipe_001', 'version': '0', 'class_name': 'datapipe_1', 'module': 'mein_test', 'function': 'test3', 'error_type': 'ValueError', 'error_message': 'TEST3_ERROR', 'timestamp': '2026-11-01T21:07:07.323008', 'line': 290, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/healer.py", line 290, in wrapper\n    result = func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 19, in test3\n    raise ValueError("TEST3_ERROR")\nValueError: TEST3_ERROR\n', 'status': 'fixed', 'fixed_at': '2026-11-01T21:07:07.324695'}]
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
        self.error_memory = [{'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-11-01T21:02:22.001409', 'line': 291, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/mein_test.py", line 291, in wrapper\n    result = func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 347, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n', 'status': 'fixed', 'fixed_at': '2026-11-01T21:02:22.002318'}, {'pipe_id': 'pipe_002', 'version': '0', 'class_name': 'datapipe_2', 'module': 'mein_test', 'function': 'test2', 'error_type': 'ValueError', 'error_message': 'TEST2_ERROR', 'timestamp': '2026-11-01T21:07:15.911995', 'line': 290, 'traceback': 'Traceback (most recent call last):\n  File "/workspaces/Celli/healer.py", line 290, in wrapper\n    result = func(self, *args, **kwargs)\n  File "/workspaces/Celli/mein_test.py", line 34, in test2\n    raise ValueError("TEST2_ERROR")\nValueError: TEST2_ERROR\n', 'status': 'fixed', 'fixed_at': '2026-11-01T21:07:15.913252'}]
        # ERROR_MEMORY_END
   
    def test1(self):
        print("pipe2:","test1")

    def test2(self):
        print("pipe2:","test2")
        raise ValueError("TEST2_ERROR")
    
    def test3(self):
        print("pipe2:","test3")