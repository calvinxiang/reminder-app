# Reminder App

This is a simple Reminder App built with a **React.js** frontend, a **FastAPI** backend, and **PostgreSQL** as the database. The app also uses **Redis** for task scheduling and **push notifications** to remind you of important events.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Create reminders with titles and specific dates/times.
- View all created reminders.
- Receive push notifications to be reminded of events.

## Tech Stack
- **Frontend**: React.js, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Task Scheduling**: Redis
- **Push Notifications**: Service Worker API, Web Push

## Getting Started
### Prerequisites
- **Node.js** (v14 or above)
- **Python** (v3.8 or above)
- **PostgreSQL** (v12 or above)
- **Redis**
- **Git**

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/calvinxiang/reminder-app.git
   cd reminder-app
   ```

## Running the Application
### Backend Setup
1. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Set up the PostgreSQL database**:
   - Create a new database named `reminder_app`.
   - Update the database credentials in the `.env` file.

4. **Start the Redis server**:
   ```bash
   # On Ubuntu (Linux)
   sudo service redis-server start
   ```

5. **Run the backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend Setup
1. **Navigate to the frontend folder**:
   ```bash
   cd ../frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Start the frontend**:
   ```bash
   npm start
   ```

## Environment Variables
You need to set up environment variables for both the frontend and backend.

### Backend `.env` (in `backend/` folder):
```
VAPID_PUBLIC_KEY=<YOUR_PUBLIC_VAPID_KEY>
VAPID_PRIVATE_KEY=<YOUR_PRIVATE_VAPID_KEY>
DATABASE_URL=postgresql://<username>:<password>@localhost/reminder_app
```

### Frontend `.env` (in `frontend/` folder):
```
REACT_APP_VAPID_PUBLIC_KEY=<YOUR_PUBLIC_VAPID_KEY>
```

Ensure that these `.env` files are **not pushed** to GitHub, as they contain sensitive information.

## Usage
- After starting both the frontend and backend servers, open your browser and navigate to `http://localhost:3000`.
- Use the form to create reminders and receive notifications.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).

