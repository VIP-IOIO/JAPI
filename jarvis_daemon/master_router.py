import time

class SwarmRouter:
    def __init__(self):
        # Simulated registry of connected devices in the Swarm
        self.connected_nodes = {
            "drone_1": {"status": "online", "battery": 98},
            "drone_2": {"status": "online", "battery": 95},
            "drone_3": {"status": "online", "battery": 12},
            "mac_home": {"status": "online", "battery": 100}
        }
        self.active_bridge = None  # None = Master LLM is active

    def process_message(self, message):
        msg_lower = message.lower().strip()

        # ==========================================
        # 1. THE ESCAPE HATCH (Disconnecting)
        # ==========================================
        # Even if bridged, the Router intercepts escape commands
        if self.active_bridge and msg_lower in ["disconnect", "exit", "jarvis disconnect", "return to master"]:
            print(f"🔌 [Router]: Terminating direct connection to {self.active_bridge}...")
            self.active_bridge = None
            return "Bridge closed. Master Jarvis is back online."

        # ==========================================
        # 2. PASSTHROUGH MODE (Token-Free)
        # ==========================================
        if self.active_bridge:
            # Bypass the Master LLM completely. Send raw text to the remote Daemon.
            print(f"🌉 [Bridge -> {self.active_bridge}]: Transmitting raw command: '{message}'")
            time.sleep(0.5) # Simulate network latency
            return f"[{self.active_bridge}]: Command received and executed."

        # ==========================================
        # 3. MASTER MODE (Routing & Global Intents)
        # ==========================================
        
        # Intent: Connect to a specific node
        if msg_lower.startswith("connect to"):
            target = msg_lower.split("connect to ")[-1].strip().replace(" ", "_")
            if target in self.connected_nodes:
                self.active_bridge = target
                return f"🔗 Bridged to {target}. Master LLM is now asleep. Type 'disconnect' to return."
            else:
                return f"⚠️ Error: Node '{target}' is offline or does not exist."

        # Intent: Gather data from ALL Jarvis nodes
        if "gather data" in msg_lower or "status of all" in msg_lower:
            print("📡 [Router]: Broadcasting status ping to the entire Swarm...")
            time.sleep(1) # Wait for network responses
            # Master LLM aggregates the JSON responses into human text
            report = "\n".join([f"   - {k}: {v['status']} (Battery: {v['battery']}%)" for k, v in self.connected_nodes.items()])
            return f"📊 [Master LLM Aggregation]: Here is the Swarm status:\n{report}"

        # Intent: Massive Swarm Coordination (Drone Show)
        if "drone show" in msg_lower and "animal" in msg_lower:
            print("🧠 [Master LLM]: Calculating 3D spatial matrix for 'Animal' formation...")
            time.sleep(2)
            print("📡 [Router]: Chunking mission file and uploading specific waypoints to all 1,000 drones...")
            time.sleep(1)
            return "✨ [Master LLM]: Mission uploaded successfully. 1,000 drones will execute the formation precisely at 21:00:00 UTC."

        # Default Intent: General Chat / Coding
        print("🧠 [Master LLM]: Processing general query...")
        return f"I am Master Jarvis. I processed your message: '{message}'. How can I assist you further?"


if __name__ == "__main__":
    print("🌐 Jarvis Prime (Master Router) Initialized.")
    router = SwarmRouter()
    
    while True:
        try:
            user_input = input("\n[Tony]: ")
            if not user_input: continue
            
            response = router.process_message(user_input)
            print(f"[Jarvis]: {response}")
            
        except KeyboardInterrupt:
            print("\nShutting down Master Router.")
            break
