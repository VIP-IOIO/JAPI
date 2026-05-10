# ==========================================
# STAGE 1: Build the Rust Daemon (Nervous System)
# ==========================================
FROM rust:1.75-slim as builder

WORKDIR /usr/src/jarvis

# Copy the Rust project files
COPY Cargo.toml ./
# (Assuming Cargo.lock might not exist yet, we just copy Cargo.toml)
COPY src ./src

# Compile the daemon for maximum performance
RUN cargo build --release

# ==========================================
# STAGE 2: The Drone Environment (The Brain)
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Install standard embedded Linux utilities
RUN apt-get update && apt-get install -y \
    procps \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the dependencies the Agent Core LLM would need
# e.g., pymavlink (to talk to Pixhawk), openai, etc.
RUN pip install --no-cache-dir requests 

# Copy the compiled Rust Daemon from the builder stage
COPY --from=builder /usr/src/jarvis/target/release/jarvis_daemon /app/jarvis_daemon

# Copy the Drone Agent script and rename it to 'agent_core.py' so the daemon finds it
COPY drone_core.py /app/agent_core.py

# Simulate the Drone's hardware state via Environment Variables
ENV JARVIS_DEVICE_TYPE="SIMULATED_DOCKER_DRONE"
ENV JARVIS_SYS_BATTERY_PERCENT="88"

# When the drone powers on, the Rust Daemon is the very first thing to start
CMD ["/app/jarvis_daemon"]
