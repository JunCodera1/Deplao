# Deplao Messenger

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A real-time chat application inspired by Telegram, built with a Python (PySide6) desktop client and a powerful Node.js backend.

![Deplao Application Screenshot](https://via.placeholder.com/800x500.png?text=Add+your+application+screenshot+here)
*(Hint: Replace the link above with an actual screenshot of your application.)*

---

## 🌟 Key Features

- **User Authentication:** Secure registration and login using JWT.
- **One-to-One Chat:** Real-time, two-way messaging.
- **File & Image Sharing:** Easily upload and share files and images.
- **Chat History:** Load and view past messages.
- **User Search:** Find and start conversations with new users.
- **Modern UI:** A beautiful and easy-to-use user interface built with PySide6.
- **Status Indicators (Coming Soon):**
    - Online/offline status.
    - Typing indicator.
    - Read receipts.

## 🛠️ Tech Stack

| Component    | Technology                                               |
|--------------|----------------------------------------------------------|
| 🖥️ **Frontend** | Python, PySide6, `python-socketio`, `requests`           |
| ⚙️ **Backend**  | Node.js, Express.js, Socket.IO, PostgreSQL, JWT, Multer |
| 🗄️ **Database** | PostgreSQL                                               |

## 🚀 Getting Started & Installation

Follow these steps to set up the development environment and run the application.

### **Prerequisites**
- **Node.js** (v16 or later)
- **Python** (v3.10 or later)
- **PostgreSQL**

---

### **1. Backend Setup**

Open a terminal and follow these steps:

**a. Clone the Repository (if you haven't already):**
```bash
git clone <your-repository-url>
cd Deplao
```

**b. Database Setup:**
- Log in to `psql` and create the database:
  ```sql
  CREATE DATABASE deplao_chat;
  ```
- Create the necessary tables by running the schema file:
  ```bash
  psql -U <your_postgres_user> -d deplao_chat -f backend_chat/schema.sql
  ```
  *(Replace `<your_postgres_user>` with your PostgreSQL username, e.g., `postgres`)*

**c. Configure Environment:**
- Copy the `.env.example` file (if it exists) to `.env`, or create a new file named `backend_chat/.env`.
- Open `backend_chat/.env` and fill in the required information, especially `DB_PASSWORD`.
  ```
  DB_USER=postgres
  DB_HOST=localhost
  DB_DATABASE=deplao_chat
  DB_PASSWORD=your_postgres_password
  DB_PORT=5432

  JWT_SECRET=your_super_secret_jwt_key
  PORT=3000
  ```

**d. Install Dependencies & Run Server:**
```bash
cd backend_chat
npm install
node index.js
```
If successful, you will see the message `Server listening on port 3000`. **Keep this terminal open.**

---

### **2. Frontend Setup**

Open a **new terminal** in the project's root directory (`Deplao`).

**a. Create and Activate Virtual Environment:**
Due to your system's configuration, a virtual environment is recommended.
```bash
# Create the virtual environment
python -m venv venv

# Activate it (on Linux/macOS)
source venv/bin/activate
# On Windows, use: venv\Scripts\activate
```

**b. Install Dependencies:**
Use the full path command (recommended for your system) to ensure packages are installed correctly:
```bash
Deplao/venv/bin/python -m pip install -r requirements.txt
```
*(If you have successfully activated the virtual environment, you might just need to run `pip install -r requirements.txt`)*

**c. Run the Application:**
Use the Python from your virtual environment to launch the UI:
```bash
Deplao/venv/bin/python main.py
```
The Login/Register window will appear.

## 🤝 Contributing

We welcome all contributions! Please follow the "Feature Branch Workflow":

1.  Never commit directly to the `main` branch.
2.  Create a new branch for each feature or bugfix: `git checkout -b feature/feature-name`.
3.  Make your changes and create small, meaningful commits on your branch.
4.  Push your branch to the remote repository: `git push origin feature/feature-name`.
5.  Create a **Pull Request** on GitHub/GitLab for code review before merging into `main`.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.