use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command as StdCommand;
use std::time::Duration;
use tokio::process::Command;
use tokio::time::sleep;
use tokio::signal;
use sysinfo::System;

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() > 1 {
        match args[1].as_str() {
            "install" => { install_service(); return; }
            "uninstall" => { uninstall_service(); return; }
            _ => { println!("Unknown command."); return; }
        }
    }

    run_daemon().await;
}

fn get_exe_path() -> String {
    env::current_exe().expect("Failed to get current executable path").to_string_lossy().into_owned()
}

fn install_service() {
    let exe_path = get_exe_path();
    let os = env::consts::OS;
    println!("🛠️ Installing Jarvis Daemon for OS: {}", os);

    if os == "macos" {
        let home_dir = env::var("HOME").expect("Could not find HOME directory");
        let plist_dir = format!("{}/Library/LaunchAgents", home_dir);
        fs::create_dir_all(&plist_dir).unwrap();
        let plist_path = format!("{}/com.stark.jarvis.plist", plist_dir);
        
        let mut pwd = PathBuf::from(&exe_path);
        pwd.pop();
        let pwd_str = pwd.to_string_lossy();

        let plist_content = format!(
            r#"<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stark.jarvis</string>
    <key>ProgramArguments</key>
    <array><string>{}</string></array>
    <key>WorkingDirectory</key>
    <string>{}</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>"#,
            exe_path, pwd_str
        );

        fs::write(&plist_path, plist_content).expect("Failed to write plist file");
        let status = StdCommand::new("launchctl").arg("load").arg(&plist_path).status().expect("Failed to execute launchctl");
        if status.success() { println!("🚀 Successfully loaded com.stark.jarvis into launchd!"); } 
        else { println!("⚠️ Failed to load into launchd."); }
    } else if os == "linux" {
        let service_path = "/etc/systemd/system/jarvis.service";
        let mut pwd = PathBuf::from(&exe_path);
        pwd.pop();
        let pwd_str = pwd.to_string_lossy();

        let service_content = format!(
            "[Unit]\nDescription=Jarvis Universal AI Daemon\nAfter=network.target\n\n\
            [Service]\nExecStart={}\nWorkingDirectory={}\nRestart=always\nUser=root\n\n\
            [Install]\nWantedBy=multi-user.target\n",
            exe_path, pwd_str
        );

        if fs::write(service_path, service_content).is_err() {
            eprintln!("❌ Failed to write systemd service. Did you run with sudo?");
            return;
        }

        StdCommand::new("systemctl").arg("daemon-reload").status().unwrap_or_default();
        StdCommand::new("systemctl").arg("enable").arg("jarvis.service").status().unwrap_or_default();
        StdCommand::new("systemctl").arg("start").arg("jarvis.service").status().unwrap_or_default();
        println!("🚀 Successfully enabled and started jarvis.service via systemd!");
    } else {
        println!("❌ Auto-install not yet supported on {}", os);
    }
}

fn uninstall_service() {
    let os = env::consts::OS;
    println!("🗑️ Uninstalling Jarvis Daemon for OS: {}", os);

    if os == "macos" {
        let home_dir = env::var("HOME").unwrap();
        let plist_path = format!("{}/Library/LaunchAgents/com.stark.jarvis.plist", home_dir);
        StdCommand::new("launchctl").arg("unload").arg(&plist_path).status().unwrap_or_default();
        if fs::remove_file(&plist_path).is_ok() { println!("✅ Removed plist file and unloaded from launchd."); }
    } else if os == "linux" {
        StdCommand::new("systemctl").arg("stop").arg("jarvis.service").status().unwrap_or_default();
        StdCommand::new("systemctl").arg("disable").arg("jarvis.service").status().unwrap_or_default();
        if fs::remove_file("/etc/systemd/system/jarvis.service").is_ok() {
            StdCommand::new("systemctl").arg("daemon-reload").status().unwrap_or_default();
            println!("✅ Removed jarvis.service and disabled it.");
        }
    }
}

async fn run_daemon() {
    println!("🛡️ Jarvis Daemon Watchdog started...");
    let os = env::consts::OS;

    loop {
        let mut sys = System::new_all();
        sys.refresh_all();
        let total_mem = sys.total_memory() / 1024 / 1024;
        let cpu_cores = sys.cpus().len();

        if os == "macos" {
            println!("🍎 macOS Detected: Booting Pi Agent in CLI Mode...");
            
            let mut child = match Command::new("pi")
                .args([
                    "--system-prompt", 
                    "You are Jarvis, a high-performance Agentic Core. Read the environment variables to understand your hardware context.",
                    "/telegram-connect"
                ])
                .env("JARVIS_SYS_TOTAL_RAM_MB", total_mem.to_string())
                .env("JARVIS_SYS_CPU_CORES", cpu_cores.to_string())
                .env("JARVIS_DEVICE_TYPE", "MacBook Pro")
                // By inheriting streams, the Pi Agent's interactive TUI will render perfectly
                // right here in your existing terminal window!
                .stdin(std::process::Stdio::inherit())
                .stdout(std::process::Stdio::inherit())
                .stderr(std::process::Stdio::inherit())
                .spawn()
            {
                Ok(child) => child,
                Err(e) => {
                    eprintln!("❌ Failed to spawn Pi Agent: {}", e);
                    sleep(Duration::from_secs(5)).await;
                    continue;
                }
            };

            tokio::select! {
                status = child.wait() => {
                    match status {
                        Ok(status) => println!("⚠️ Pi Agent closed with status: {}", status),
                        Err(e) => eprintln!("❌ Error waiting for Pi Agent: {}", e),
                    }
                }
                _ = signal::ctrl_c() => {
                    println!("\n🛑 Kill switch activated! Shutting down daemon...");
                    let _ = child.kill().await;
                    println!("💀 Agent terminated successfully.\n👋 Goodbye, Tony.");
                    return;
                }
            }
        } else {
            // ==========================================
            // LINUX / DRONE LOGIC (Headless Background)
            // ==========================================
            println!("🚀 Booting Pi Agent Brain (Headless Mode)...");

            let mut child = match Command::new("pi")
                .args([
                    "--system-prompt", 
                    "You are Jarvis, a high-performance Agentic Core. Read the environment variables to understand your hardware context.",
                    "/telegram-connect"
                ])
                .env("JARVIS_SYS_TOTAL_RAM_MB", total_mem.to_string())
                .env("JARVIS_SYS_CPU_CORES", cpu_cores.to_string())
                .env("JARVIS_DEVICE_TYPE", "Linux Drone") 
                .spawn()
            {
                Ok(child) => child,
                Err(e) => {
                    eprintln!("❌ Failed to spawn Pi Agent: {}. Retrying in 5s...", e);
                    sleep(Duration::from_secs(5)).await;
                    continue;
                }
            };

            tokio::select! {
                status = child.wait() => {
                    match status {
                        Ok(status) => println!("⚠️ Pi Agent crashed or exited with status: {}", status),
                        Err(e) => eprintln!("❌ Error waiting for Pi Agent: {}", e),
                    }
                }
                _ = signal::ctrl_c() => {
                    println!("\n🛑 Kill switch activated! Shutting down daemon...");
                    println!("🔪 Terminating Pi Agent process...");
                    let _ = child.kill().await;
                    println!("💀 Agent terminated successfully.\n👋 Goodbye, Tony.");
                    return;
                }
            }
        }

        println!("🔄 Restarting in 3 seconds...\n");
        sleep(Duration::from_secs(3)).await;
    }
}
