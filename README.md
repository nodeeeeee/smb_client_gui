# NUS SoC Print GUI

A modern, Material Design desktop application for NUS SoC students to easily print documents via the `smbclient` service on Linux. No more wrestling with command-line strings—just select your file, pick a printer, and print.

## ✨ Features

*   **Google Material Design UI**: A clean, intuitive interface built with PyQt5.
*   **Integrated Printer List**: Full details (location, model, and name) for all SoC print queues.
*   **Credential Management**: Securely save your NUSNET usernames and passwords so you only have to type them once.
*   **Intelligent Defaults**: Remembers your last used printer for faster printing.
*   **Quick Links**: One-click access to check your printing quota (via ePrint) and buy additional quota (via SoC Pay).
*   **Native Linux Support**: Optimized for Linux environments with automatic dependency checks.

## 🚀 Getting Started

### Prerequisites

You must have `smbclient` installed on your system. On Ubuntu/Debian, run:

```bash
sudo apt update
sudo apt install smbclient
```

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/smb_client_gui.git
    cd smb_client_gui
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install PyQt5
    ```

### Usage

Run the application using the following command:

```bash
PYTHONPATH=src python3 src/gui.py
```

1.  **Add your Account**: On the first run, go to **Manage Accounts** and add your NUSNET username (e.g., `e1234567`) and password.
2.  **Select Document**: Click **Browse** to choose the file you want to print.
3.  **Choose Printer**: Select a printer from the searchable dropdown list.
4.  **Print**: Click **Print Document**. The app will handle the authentication and transmission to the SoC print server.

## 🛠 Project Structure

*   `src/gui.py`: The PyQt5-based frontend and main entry point.
*   `src/cli_forge.py`: Handles the generation and execution of `smbclient` shell commands.
*   `src/config.py`: Manages persistent local storage for credentials and settings (stored in `~/.smb_client_gui.json`).

## 🔒 Security

*   **Local Storage**: Credentials are stored locally on your machine in your home directory.
*   **Encrypted Transmission**: The app uses the standard `smbclient` protocol to transmit documents to `nts27.comp.nus.edu.sg`.

## 📄 License

This project is intended for NUS SoC students. Please follow the [SoC Computing Policy](https://it.comp.nus.edu.sg/policy/) when using the printing services.
