# Rust Agent Core: The Programmer Extension

**Environment:** MacBook Pro or Linux Developer Desktop.
**Goal:** System-level development, code refactoring, and server management.

## Boot Sequence
1. The **Rust Daemon** boots via macOS `launchd`. 
2. The Daemon injects `JARVIS_DEVICE_TYPE=MacBook_Pro` and starts the **Rust Agentic Core**.
3. The Agentic Core loads the `jarvis_desktop_extension.wasm` plugin.

## The Programmer Extension (Capabilities)
Because the Core is written in Rust, it has native, high-speed access to the OS filesystem, vastly surpassing Python's capabilities.
- **Tool:** `grep_ast` (Instant codebase search and Abstract Syntax Tree parsing).
- **Tool:** `cargo_build` / `npm_run` (Native OS process spawning and memory monitoring).
- **Comm Protocol:** Connects seamlessly to a Telegram Bot API or a local desktop Terminal UI.

## The User Journey
* **Tony (via Telegram):** "My Node server crashed. Fix it."
* **Agentic Core:** Uses the extension to instantly read syslog and parse the error.
* **Agentic Core:** Identifies a port conflict. Finds the conflicting PID using native Rust system calls.
* **Agentic Core:** Kills the PID, restarts the server natively, and replies on Telegram: *"Port cleared. Server restarted."*
