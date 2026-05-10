fn main() {
    std::process::Command::new("pi").args(["--help"]).stdin(std::process::Stdio::inherit()).stdout(std::process::Stdio::inherit()).stderr(std::process::Stdio::inherit()).spawn().unwrap().wait().unwrap();
}
