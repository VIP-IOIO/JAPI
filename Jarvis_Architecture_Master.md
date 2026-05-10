# Jarvis Ecosystem Master Architecture

This document maps out the current functional architecture as well as the future roadmap for the polymorphic Jarvis ecosystem. It illustrates how the "Nervous System" (Daemon) couples with either the current `pi` agent or the future Rust-native Agentic Core.

## 1. Ecosystem Overview

```mermaid
graph TD
    %% Define Styles
    classDef daemon fill:#e06666,stroke:#990000,stroke-width:2px,color:#fff;
    classDef currentAgent fill:#6d9eeb,stroke:#1155cc,stroke-width:2px,color:#fff;
    classDef futureAgent fill:#93c47d,stroke:#38761d,stroke-width:2px,color:#fff,stroke-dasharray: 5 5;
    classDef hardware fill:#b4a7d6,stroke:#351c75,stroke-width:2px,color:#fff;

    %% 1. Hardware Layer
    subgraph Hardware_Layer [1. The Physical Bodies]
        direction LR
        Mac[Desktop / Mac]
        Drone[Military Quadcopter / Linux]
        EV[Electric Vehicle]
    end
    class Mac,Drone,EV hardware;

    %% 2. Watchdog Layer
    subgraph Nervous_System [2. Rust Daemon Watchdog - CURRENT]
        Watchdog[Jarvis Daemon]
        SysMonitor[sysinfo Telemetry Scanner]
        Injector[Env Var Injector]
        
        Watchdog --> SysMonitor
        SysMonitor --> Injector
    end
    class Watchdog,SysMonitor,Injector daemon;

    %% 3. Current Agent Layer
    subgraph Current_Brain [3. The Pi Agent - CURRENT SCOPE]
        Pi[Generic 'pi' CLI]
        PiTelegram[Telegram Extension]
        PiTools[Generic Coding Tools]
        
        Pi --> PiTelegram
        Pi --> PiTools
    end
    class Pi,PiTelegram,PiTools currentAgent;

    %% 4. Future Agent Layer
    subgraph Future_Brain [4. Rust Agentic Core - FUTURE SCOPE]
        RustCore[Native Rust LLM Core]
        WasmLoader[WASM Plugin Engine]
        
        subgraph Modular_Extensions [Dynamic WASM Plugins]
            DroneExt[drone_ext.wasm <br> MAVLink / GPS]
            MacExt[desktop_ext.wasm <br> FileSystem / OS]
            EVExt[ev_ext.wasm <br> CAN Bus / Sensors]
        end
        
        RustCore --> WasmLoader
        WasmLoader --> DroneExt
        WasmLoader --> MacExt
        WasmLoader --> EVExt
    end
    class RustCore,WasmLoader,DroneExt,MacExt,EVExt futureAgent;

    %% Connect the layers
    Mac --> Watchdog
    Drone --> Watchdog
    EV --> Watchdog

    Injector -->|Injects Env Vars & Spawns| Pi
    Injector -.->|Future: Spawns Native Binary| RustCore
```

## 2. Current Scope (What is working today)

The system currently operates flawlessly as a decoupling of **Hardware Management** and **Agentic Logic**.

1. **The Daemon (Rust):** Starts on system boot via macOS `launchd` or Linux `systemd`. It scans the system using `sysinfo`, determines CPU/RAM, and injects `JARVIS_DEVICE_TYPE`.
2. **The Brain (Node/Pi):** The Daemon spawns the generic `pi` CLI. 
   - On Mac, it visually pops open `Terminal.app` to provide an interactive developer experience.
   - On Linux (Drone), it runs entirely headlessly in the background.
3. **The Limitation:** The `pi` tool is primarily designed for desktop coding assistance. It is single-threaded (Node.js) and somewhat heavy for an embedded military drone.

## 3. Future Scope (The Native Evolution)

To achieve microsecond latency, absolute memory safety, and 100% offline edge-computing capability, the "Brain" will be completely rewritten in Rust.

1. **Rust Agentic Core:** A custom binary that replaces the `pi` tool. It natively queries local models (e.g., Llama.cpp) and maintains conversation memory.
2. **WASM Polymorphism:** Instead of bloated Python or Node extensions, capabilities are distributed as highly compressed WebAssembly (`.wasm`) plugins.
   - When the Daemon injects `JARVIS_DEVICE_TYPE=Military_Quadcopter`, the Rust Core instantly loads `drone_ext.wasm` into a secure sandbox, gaining the ability to fly.
3. **Encrypted Mesh Radio:** Moving away from standard internet APIs (like Telegram), the Rust Core will use Silvus or TrellisWare mesh radios to communicate directly with Tony's device, ensuring operation in denied environments.
