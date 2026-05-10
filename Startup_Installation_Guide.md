# Jarvis Auto-Start Installation Guide

The Rust Daemon now has self-installing capabilities. It can automatically detect whether it is running on macOS (`launchd`) or Linux (`systemd`), generate the required background configuration files, and hook itself into the OS boot sequence.

## 🛠 Step 1: Compile the Daemon
Before installing, you must compile the final production binary. Navigate to the `jarvis_daemon` folder in your terminal and run:

```bash
cargo build --release
```

This creates a standalone executable file at `./target/release/jarvis_daemon`.

## 🚀 Step 2: Install to Startup
Run the compiled binary with the `install` flag.

**On Mac:**
```bash
./target/release/jarvis_daemon install
```
*(This automatically creates `~/Library/LaunchAgents/com.stark.jarvis.plist` and loads it. The agent will now boot in the background every time you log in).*

**On Linux (Raspberry Pi/Drone):**
```bash
sudo ./target/release/jarvis_daemon install
```
*(This automatically creates `/etc/systemd/system/jarvis.service` and enables it).*

## 🛑 Step 3: The Kill Switch (Uninstall)
If you want to stop the agent from running in the background and remove it from the startup sequence completely, run:

**On Mac:**
```bash
./target/release/jarvis_daemon uninstall
```

**On Linux:**
```bash
sudo ./target/release/jarvis_daemon uninstall
```

*(This gracefully stops the agent, kills the python script, and deletes the OS configuration files).*
