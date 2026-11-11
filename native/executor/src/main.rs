//! Native execution of scientific programs, independent of any agent host.
use serde_json::Value;
use std::io;
#[cfg(windows)]
use std::process::Stdio;
use tokio::{io::AsyncWriteExt, process::Child};
#[cfg(windows)]
use tokio::process::Command;
mod job;
mod process_tree;

pub(crate) async fn emit(value: &Value) -> io::Result<()> {
    let mut output = tokio::io::stdout();
    output.write_all(format!("{value}\n").as_bytes()).await?;
    output.flush().await
}

pub(crate) async fn stop(child: &mut Child) {
    if let Some(id) = child.id() {
        #[cfg(unix)]
        unsafe { libc::kill(-(id as i32), libc::SIGKILL); }
        #[cfg(windows)]
        {
            let _ = Command::new("taskkill").args(["/PID", &id.to_string(), "/T", "/F"])
                .stdout(Stdio::null()).stderr(Stdio::null()).status().await;
        }
    }
    let _ = child.kill().await;
    let _ = child.wait().await;
}

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    if std::env::args().nth(1).as_deref() == Some("--version") {
        println!("optics-execd {}", env!("CARGO_PKG_VERSION"));
        return Ok(());
    }
    job::run().await
}
