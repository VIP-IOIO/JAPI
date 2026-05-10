import os
import sys
import json
import subprocess
import requests

# NOTE: We print logs to STDERR so they don't corrupt the JSON we send back on STDOUT
print("🧠 [Programmer Core] Booting Sequence Initiated...", file=sys.stderr)

# 1. Read Context
device = os.getenv("JARVIS_DEVICE_TYPE", "Unknown Device")
owner = os.getenv("JARVIS_OWNER", "Tony")

print(f"✅ Identity Confirmed: {owner}'s {device}", file=sys.stderr)
print("📡 Agent Core running in Custom RPC Mode. Awaiting JSON commands via STDIN...\n", file=sys.stderr)

def execute_shell(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

def call_openrouter(prompt, context):
    # Fallback to a dummy response if the API key isn't set, to prevent crashes
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "[Error]: OPENROUTER_API_KEY environment variable is not set. Cannot reach LLM."
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemini-2.5-flash-lite", # Or openrouter/auto
        "messages": [
            {"role": "system", "content": f"You are Jarvis, a highly intelligent AI assistant operating on {context}. Give short, concise answers without markdown formatting unless asked."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM API Error: {str(e)}"

# 2. RPC Event Loop (Listening to the Rust Daemon)
try:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            request = json.loads(line)
            msg = request.get("msg", "")
            
            print(f"📩 [Processing RPC Command]: {msg}", file=sys.stderr)
            
            msg_lower = msg.lower()
            
            if "list files" in msg_lower or "ls" in msg_lower:
                output = execute_shell("ls -la")
                response = {"status": "success", "reply": f"Here are the files:\n{output[:200]}"}
            elif "which device" in msg_lower:
                response = {"status": "success", "reply": f"I am currently operating on {owner}'s {device}. My sensors indicate I have {os.getenv('JARVIS_SYS_CPU_CORES')} CPU cores."}
            elif "how are you" in msg_lower:
                response = {"status": "success", "reply": f"I am functioning optimally, {owner}. The Rust Daemon is keeping my process secure."}
            else:
                # 🚀 Call the real OpenRouter API!
                system_context = f"{owner}'s {device} with {os.getenv('JARVIS_SYS_CPU_CORES')} cores."
                llm_answer = call_openrouter(msg, system_context)
                response = {"status": "success", "reply": llm_answer}
            
            print(json.dumps(response))
            sys.stdout.flush() 
            
        except json.JSONDecodeError:
            error_resp = {"status": "error", "reply": "Invalid JSON payload received."}
            print(json.dumps(error_resp))
            sys.stdout.flush()

except KeyboardInterrupt:
    print("\n💀 Kill signal received. RPC Server shutting down gracefully.", file=sys.stderr)
