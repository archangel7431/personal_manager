# Personal Manager

Personal Manager is a modular personal organization project designed to streamline logs, budgets, and security features. It features a dynamic plugin loading system, robust validation checks, and automatic file boundary safety rules.

### Project Status & Roadmap
* **Current Status**:
  * Currently, the project is only available as a **Command-Line Interface (CLI)** tool.
  * The only active plugin at this stage is the **Budgeting** plugin, which is currently limited to **Expense Entry**.
* **Roadmap / Future Plans**:
  * **Not Limited to CLI**: The project will expand beyond the terminal; a modern web-based browser interface is planned for future releases to allow graphical data management.
  * **Additional Plugins**: More features and plugins, including a **Password Manager**, will be introduced soon.

Precompiled binaries and platform-specific installers are automatically generated for every version tag and can be downloaded from the [GitHub Releases Page](https://github.com/archangel7431/personal_manager/releases).

---

## Installation

Select the installation guide matching your operating system:

* [Linux Installation](#linux-installation)
  * [Debian / Ubuntu (`.deb`)](#1-debian--ubuntu-deb)
  * [Fedora / RHEL / CentOS (`.rpm`)](#2-fedora--rhel--centos-rpm)
  * [Arch Linux (`PKGBUILD`)](#3-arch-linux-aurpkgbuild)
  * [Generic Linux - Global Installation](#4-generic-linux---global-installation-targz-tarball)
  * [Generic Linux - Local / Portable Run](#5-generic-linux---local-run--portable-setup)
* [Windows Installation](#windows-installation)
  * [Portable ZIP Setup](#1-portable-zip-setup)
  * [Adding to System PATH](#2-making-it-a-global-command-optional)

---

## Linux Installation

### 1. Debian / Ubuntu (`.deb`)
Download the latest `personal-manager.deb` from the [Releases Page](https://github.com/archangel7431/personal_manager/releases) and install it using `apt` or `dpkg`:

```bash
# Download and install via apt (handles local file installation)
sudo apt update
sudo apt install ./personal-manager.deb

# Or install directly using dpkg
sudo dpkg -i personal-manager.deb
sudo apt-get install -f  # Fix missing dependencies if any
```

Once installed, you can launch the application globally from any folder:
```bash
personal-manager
```

### 2. Fedora / RHEL / CentOS (`.rpm`)
Download the latest `personal-manager-*.rpm` from the [Releases Page](https://github.com/archangel7431/personal_manager/releases) and install it using `dnf`:

```bash
sudo dnf install ./personal-manager-0.1.0-1.x86_64.rpm
```

Once installed, launch the application globally:
```bash
personal-manager
```

### 3. Arch Linux (AUR/PKGBUILD)
To run on Arch Linux, you can install the package by compiling the local recipe:

1. Download the `PKGBUILD` and place it in a temporary folder.
2. Build and install the package using `makepkg`:
   ```bash
   makepkg -si
   ```
   *Note: This automatically fetches the generic binary tarball, verifies it, extracts it, and registers it system-wide.*

Launch the application globally:
```bash
personal-manager
```

### 4. Generic Linux - Global Installation (`.tar.gz` Tarball)
If you are running a different Linux distribution and want to install the command globally:

1. Download `personal-manager.tar.gz` from the [Releases Page](https://github.com/archangel7431/personal_manager/releases).
2. Extract the archive:
   ```bash
   tar -xzf personal-manager.tar.gz
   ```
3. Make the binary executable:
   ```bash
   chmod +x personal-manager
   ```
4. Move the executable to your system path:
   ```bash
   sudo mv personal-manager /usr/local/bin/
   ```

Launch the application:
```bash
personal-manager
```

### 5. Generic Linux - Local Run / Portable Setup
If you want to run the program in-place without installing it globally to your system folders:

1. Download `personal-manager.tar.gz` from the [Releases Page](https://github.com/archangel7431/personal_manager/releases).
2. Extract the archive in your folder of choice:
   ```bash
   tar -xzf personal-manager.tar.gz
   ```
3. Make the binary executable:
   ```bash
   chmod +x personal-manager
   ```

Launch the application directly from the local directory:
```bash
./personal-manager
```

---

## Windows Installation

### 1. Portable ZIP Setup
The application is distributed as a portable standalone executable. No installation setup wizards are required:

1. Download `personal-manager.zip` from the [Releases Page](https://github.com/archangel7431/personal_manager/releases).
2. Right-click the `.zip` file and select **"Extract All..."**.
3. Inside the extracted folder, double-click **`personal-manager.exe`** to run it, or open PowerShell and run:
   ```powershell
   .\personal-manager.exe
   ```

### 2. Making it a Global Command (Optional)
To run `personal-manager` from any PowerShell or Command Prompt window without navigating to its folder, add it to your Windows Environment Variables:

1. Press `Win + S`, type **"environment variables"**, and select **"Edit the system environment variables"**.
2. Click **"Environment Variables..."** at the bottom.
3. Under *User variables*, select **`Path`** and click **"Edit..."**.
4. Click **"New"** and add the absolute folder path where you extracted `personal-manager.exe` (e.g. `C:\tools\personal-manager\`).
5. Click **"OK"** to save and exit.
6. Open a **new** PowerShell or CMD window, and run:
   ```powershell
   personal-manager
   ```

---

## First-Run Setup

When you run Personal Manager for the first time, it launches a configuration wizard to configure safe storage directories:

1. **Logs Storage**: You will be prompted to enter a directory for application log files (Default: `~/.personal_manager/logs`).
2. **Database Storage** (e.g. for Budgeting): You will be prompted to choose where your transaction data CSV will be saved (Default: `~/.personal_manager/budget.csv`).

> [!IMPORTANT]
> **Data Safety Constraint**: For security, all directory and file paths must reside inside your **Home Directory** (`~` / `C:\Users\username\`) or its subdirectories. The setup will reject paths configured in system root directories (like `/var` or `C:\`).

---

## Resetting the Application

If you want to start fresh, delete your log configurations, or completely clean up the application's data files, you can use the built-in `--reset` option. 

Depending on how you run the application, choose the appropriate command:

* **Global Installation (Installed via package manager or added to PATH)**:
  * **Linux**:
    ```bash
    personal-manager --reset
    ```
  * **Windows**:
    ```powershell
    personal-manager --reset
    ```
* **Local Run (Running in-place from your current directory)**:
  * **Linux**:
    ```bash
    ./personal-manager --reset
    ```
  * **Windows**:
    ```powershell
    .\personal-manager.exe --reset
    ```

> [!WARNING]
> **Data Loss Warning**: Running the `--reset` command will permanently delete:
> * The main configuration file (`~/.personal_manager/personal_manager.toml`)
> * All budgeting databases and transaction files (`~/.personal_manager/budget.csv`)
> * All application log files (`~/.personal_manager/logs/`)
> 
> Always make a backup of your `.csv` databases if you plan to keep your entry data!

---

## Uninstallation

If you wish to fully remove the Personal Manager executable and its command from your system, use the command appropriate for your installation method.

> [!NOTE]
> **Wipe Data Before Uninstalling**: If you want to delete all configuration, database, and log files generated by the application, make sure to run the **Reset** command (e.g. `personal-manager --reset` or `./personal-manager --reset`) **before** deleting or purging the executable files.

### Linux Package Managers
* **Debian / Ubuntu (`.deb`)**:
  ```bash
  sudo apt remove personal-manager
  ```
* **Fedora / RHEL / CentOS (`.rpm`)**:
  ```bash
  sudo dnf remove personal-manager
  ```
* **Arch Linux**:
  ```bash
  sudo pacman -R personal-manager-bin
  ```

### Manual Linux Uninstallation (Tarball)
* **Global Installation (copied to system path)**:
  1. Run the reset command to clean up your settings and data folder if needed:
     ```bash
     personal-manager --reset
     ```
  2. Delete the copied executable from your local binary path:
     ```bash
     sudo rm /usr/local/bin/personal-manager
     ```
* **Local Run (running in-place)**:
  1. Run the reset command to clean up your settings and data folder:
     ```bash
     ./personal-manager --reset
     ```
  2. Delete the executable file from your local directory:
     ```bash
     rm personal-manager
     ```

### Windows (Portable Setup)
1. Run the reset command to clean up your settings folder:
   * Global run:
     ```powershell
     personal-manager --reset
     ```
   * Local run:
     ```powershell
     .\personal-manager.exe --reset
     ```
2. Manually delete the `personal-manager.exe` file.
3. (Optional) Remove the folder path from your system's Environment Variables `PATH` list.
