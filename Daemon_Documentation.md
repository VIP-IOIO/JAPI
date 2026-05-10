# Jarvis Universal Daemon

This is the "Nervous System" for the Jarvis AI architecture. It is a lightweight Rust daemon that runs in the background, spawns your AI Agent Core, injects system telemetry, and ensures the agent never dies.

## 🛠 How to Run on Any System

Because this is written in Rust, it does not require Python, Node.js, or any other runtime to operate. 

1. **Build the binary for your specific device:**
   ```bash
   cargo build --release
   ```
2. **Locate the executable:**
   The compiled binary will be in `./target/release/jarvis_daemon`.
3. **Run it:**
   ```bash
   ./target/release/jarvis_daemon
   ```
   *(To run it on startup, you can add this binary to your OS's startup programs, e.g., using `systemd` on Linux, `launchd` on macOS, or the Startup folder on Windows).*

---

## 🔌 How to Attach a New Agent Core

The daemon is agnostic to the language or logic of your Agent Core. It treats the Agent Core as a generic child process.

To attach a new core (e.g., swapping a Mac Coding Agent for a Drone Agent):
1. Open `src/main.rs`.
2. Change the `agent_command` and `agent_script` variables to point to your new agent's entry point.
   - For Python: `Command::new("python3").arg("my_new_agent.py")`
   - For Node: `Command::new("node").arg("my_new_agent.js")`
   - For a compiled binary: `Command::new("./my_drone_agent_binary")`

*(In future versions, this will be loaded dynamically from an `identity.yaml` config file).*

---

## 🧠 The Standard "Agent Core" Idea

What exactly *is* an Agent Core in this architecture? 

The **Standard Agent Core Interface** is a design pattern where the AI script acts purely as the "Brain", and expects the "Nervous System" (the Daemon) to handle the physical body.

### A Standard Agent Core MUST:
1. **Be a long-running process:** It should listen for inputs (e.g., Telegram Webhooks, websockets) infinitely.
2. **Expect Context via Environment Variables:** The Rust Daemon will pass system state (Battery %, CPU load) into the process via environment variables. The Agent should read these on boot and during operation.
3. **Execute Commands via System Calls:** The Agent should interact with its host machine by executing standard shell commands (`std::process::Command` in Python/Node).
4. **Die gracefully on SIGTERM:** When the Rust Daemon activates the Kill Switch, it will send a terminate signal. The Agent Core should clean up its SQLite database connections and exit.

**Example Standard Core (Python):**
```python
import os
import time

# 1. Read the environment variables injected by the Rust Daemon
device_type = os.getenv("JARVIS_DEVICE", "Unknown")
owner = os.getenv("JARVIS_OWNER", "Tony")

print(f"I am initialized on a {device_type}. Awaiting commands from {owner}.")

# 2. Infinite Loop listening for Telegram / Voice inputs
while True:
    # Listen to Telegram API...
    time.sleep(1) 
```
