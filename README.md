My Try at creating a database from scratch

This is a simple webUI with A lightweight, secure database web application built with **Flask** and **AES encryption**. Records are encrypted locally with a random AES key, ensuring that sensitive data is never stored in plaintext. This app supports user login, CRUD operations, JSON upload, and record search.

<img width="901" height="670" alt="Screenshot 2025-11-02 225445" src="https://github.com/user-attachments/assets/360730f7-93c3-4b3a-bb1e-f7658d84906e" />

## Features

- **User Authentication**: Simple login system to protect access.
- **AES-Encrypted Records**: All records are encrypted locally using AES-CBC with padding.
- **CRUD Operations**: Add, view, update, and delete records.
- **JSON Upload**: Upload JSON files to bulk add records.
- **Search**: Quickly search records by ID or content.
- **Modern UI**: Glass-like frosted background design with responsive layout.

<img width="1226" height="639" alt="Screenshot 2025-11-02 230440" src="https://github.com/user-attachments/assets/40045dc9-697c-4e5e-b4c1-decfb23d390b" />

### Prerequisites

- Python 3.8+
- pip

## Usage

Start the server with python app.py.

Navigate to /login to log in. Default dummy user:

Username: admin

Password: password

Add, view, or delete records.

Upload a JSON file to bulk import records.

## Security Notes

AES encryption key is stored locally. Protect db_key.key to avoid data loss.

Passwords are stored in plaintext in this demo. For production, use hashed passwords (e.g., bcrypt).

This app is intended for local or small-team use. Not hardened for public deployment.

## Contributing

Fork the repo.

Create a feature branch: git checkout -b feature/my-feature

Commit your changes: git commit -am 'Add new feature'

Push to the branch: git push origin feature/my-feature

Open a Pull Request
