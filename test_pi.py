import subprocess
import json

payloads = [
    {"command": "prompt", "text": "hi"},
    {"type": "prompt", "message": "hi"},
    {"action": "prompt", "message": "hi"},
    {"cmd": "prompt", "text": "hi"},
    {"msg": "hi"},
    {"request": "hi"}
]

for p in payloads:
    print(f"Testing {p}")
    proc = subprocess.Popen(['pi', '--mode', 'rpc'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(json.dumps(p) + "\n")
    print(out)
