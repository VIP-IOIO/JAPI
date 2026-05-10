# Rust Agent Core: The Drone Extension

**Environment:** Companion Computer (NVIDIA Jetson, Raspberry Pi) hardwired to a Pixhawk Flight Controller.
**Goal:** Autonomous flight, visual navigation, and denied-environment operation.

## Boot Sequence
1. The **Rust Daemon** boots on the Jetson. It detects the Pixhawk over USB.
2. The Daemon injects: `JARVIS_DEVICE_TYPE=Military_Quadcopter` and starts the **Rust Agentic Core**.
3. The Agentic Core reads the device type and dynamically loads the `jarvis_drone_extension.wasm` plugin.

## The Drone Extension (Capabilities)
Unlike a Python script, this Rust extension operates with microsecond latency, crucial for physical hardware.
- **Tool:** `mavlink_stream` (Sends 100Hz waypoint updates to Pixhawk).
- **Tool:** `vslam_compute` (Runs local computer vision for obstacle avoidance).
- **Comm Protocol:** Establishes an encrypted Silvus mesh-radio link to the user, abandoning standard internet (Telegram).

## The User Journey
* **Tony (via Radio):** "Fly 200 meters North and scan for heat signatures."
* **Agentic Core:** Generates a flight plan matrix. Uses the drone extension to stream MAVLink commands to the Pixhawk.
* **Agentic Core:** Analyzes thermal camera feed locally.
* **Agentic Core:** Returns encrypted radio message: *"Target acquired. Awaiting engagement rules."*
