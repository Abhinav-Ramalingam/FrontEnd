# Raspberry Pi Chat Application

## Overview
This project is designed to provide a basic front end for communication between two Raspberry Pi devices. The application uses Flask to serve the web interface, with Jinja2 for templating dynamic content. Tailwind CSS and DaisyUI are utilized to enhance the visual appeal of the application.

## Prerequisites
Ensure you have the following installed on your system:

- **Python** (preferably latest version)
- **pip** (Python package installer)
- **Flask** (for backend functionality)

## Installation Instructions

#### 1. Install Python

- **Linux** (Debian-based):
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

- **macOS** (using Homebrew):
  ```bash
  brew install python
  ```

#### 2. Install pip (if not already installed)

- **Linux**:
  ```bash
  sudo apt install python3-pip
  ```

- **macOS**: (pip is included with Python installation via Homebrew)

#### 3. Set Up a Virtual Environment

- **Linux and macOS**:
  ```bash
  python3 -m venv venv
  ```

#### 4. Activate the Virtual Environment

- **Linux and macOS**:
  ```bash
  source venv/bin/activate
  ```

#### 5. Install Dependencies
Run the following command to install necessary dependencies:

- **Linux and macOS**:
```bash
pip install flask 
pip install flask_socketio
pip install bcrypt
```

#### 6. Running the Project
To start the project, use the following command:

```bash
python main.py
```
