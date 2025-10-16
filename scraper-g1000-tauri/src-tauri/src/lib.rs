use std::process::{Command, Child};
use std::sync::Mutex;
use tauri::Manager;

struct PythonBackend(Mutex<Option<Child>>);

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .manage(PythonBackend(Mutex::new(None)))
    .setup(|app| {
      // Start Python backend
      let python_path = "C:\\Users\\47\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
      let backend_script = app.path().resource_dir()
        .expect("Failed to get resource dir")
        .join("..")
        .join("backend")
        .join("api_server.py");

      println!("[Tauri] Starting Python backend: {:?}", backend_script);

      let child = Command::new(python_path)
        .arg(backend_script)
        .arg("5050")
        .spawn();

      match child {
        Ok(process) => {
          println!("[Tauri] Python backend started with PID: {}", process.id());
          let backend = app.state::<PythonBackend>();
          *backend.0.lock().unwrap() = Some(process);
        }
        Err(e) => {
          eprintln!("[Tauri] Failed to start Python backend: {}", e);
        }
      }

      // Setup debug logging
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }

      Ok(())
    })
    .on_window_event(|_window, event| {
      if let tauri::WindowEvent::Destroyed = event {
        // App is closing - kill Python backend
        println!("[Tauri] Window destroyed, killing Python backend...");
      }
    })
    .build(tauri::generate_context!())
    .expect("error while building tauri application")
    .run(|app_handle, event| {
      if let tauri::RunEvent::ExitRequested { .. } = event {
        // Kill Python backend when app exits
        let backend = app_handle.state::<PythonBackend>();
        if let Some(mut child) = backend.0.lock().unwrap().take() {
          println!("[Tauri] Killing Python backend...");
          let _ = child.kill();
        }
      }
    });
}
