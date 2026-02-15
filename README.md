# TRemote - Remote PC Control Bot

TRemote is a Python-based automation tool that allows users to monitor and control their PC remotely via a Telegram Bot. It provides a secure and convenient way to manage system resources and execute power commands from anywhere in the world.

## 🚀 Features

### 🔌 Power Management
- **Remote Shutdown & Restart:** Initiate power cycles with a built-in 30-second safety countdown.
- **Sleep Mode:** Put the PC into sleep mode to save energy.
- **Command Cancellation:** Ability to abort shutdown/restart sequences if triggered by mistake.

### 📊 System Monitoring
- **Real-time Status:** Monitor **CPU usage, RAM availability, and Disk space**.
- **Network Performance:** Integrated **Internet Speedtest** to check upload/download speeds.
- **System Uptime:** View how long the computer has been running.
- **Startup Alerts:** Automatically sends an "Online" notification with the local IP and Hostname when the PC boots up.

### 🛠️ Remote Utilities
- **Screenshots:** Capture the current screen and send it directly to your Telegram chat.
- **URL Execution:** Open specific websites on the host machine's default browser.
- **App Launcher:** List and launch pre-configured applications remotely.

## 🛠 Tech Stack

- **Language:** Python 3.x
- **Bot API:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **System Monitoring:** `psutil`
- **Automation:** `PyAutoGUI` (for screenshots and interaction)
- **Network Tools:** `speedtest-cli`

![Image](https://github.com/user-attachments/assets/b88b710d-3f2c-49ff-9d5f-efe66dafc78b)

## 📂 Project Structure

```text
tremote-bot/
├── src/
│   ├── main.py          # Main bot logic
│   ├── system_tools.py  # PC control functions
│   └── monitoring.py    # Resource tracking logic
├── .env                 # API tokens and sensitive data
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
