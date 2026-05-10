import time
import sys
import os

print("🧠 Agent Core initialized.")

# Read the sensory data injected by the Rust Daemon
device_type = os.getenv("JARVIS_DEVICE_TYPE", "Unknown")
total_ram = os.getenv("JARVIS_SYS_TOTAL_RAM_MB", "0")
used_ram = os.getenv("JARVIS_SYS_USED_RAM_MB", "0")
cpu_cores = os.getenv("JARVIS_SYS_CPU_CORES", "0")

print("\n--- 📡 Sensor Data Received From Nervous System ---")
print(f"Identity        : {device_type}")
print(f"CPU Cores       : {cpu_cores}")
print(f"Memory Usage    : {used_ram} MB / {total_ram} MB")
print("---------------------------------------------------\n")

print("   Listening for events...")

try:
    for i in range(1, 6):
        print(f"   [Agent Core] Working... heartbeat {i}/5")
        time.sleep(2)
        
    print("💥 Oh no! The Agent Core encountered a fatal error and crashed!")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n   [Agent Core] Shutting down gracefully.")
    sys.exit(0)
