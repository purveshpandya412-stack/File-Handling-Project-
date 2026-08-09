# 🗂️ FileVault — File Handling System

A clean, modern **Streamlit UI** for basic file operations — Create, Read, Update, and Delete — built on top of Python's `pathlib`.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Create** — make a new file with custom content, with duplicate-name protection
- **Read** — preview any file's contents and download it directly
- **Update** — rename, append text to, or fully overwrite an existing file
- **Delete** — remove a file with a confirmation checkbox to prevent accidents
- **File Explorer sidebar** — live count and total size of all stored files, with per-file details (size, last modified)
- **Polished UI** — gradient header, card layout, and custom styling instead of a bare CLI

---

## 📸 Preview

> Run the app locally to see it in action — a dark-themed dashboard with tabs for each operation.

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/filevault.git
cd filevault
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
filevault/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── user_files/          # Auto-created folder where files are stored
└── README.md
```

---

## 🛠️ Built With

- [Python](https://www.python.org/) — `pathlib` for file operations
- [Streamlit](https://streamlit.io/) — UI framework

---

## 📌 Notes

- All files created through the app are stored in a local `user_files/` directory to keep things organized.
- This project is intended as a learning/demo tool for basic file handling concepts wrapped in a real UI.

---

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🙌 Author

Made with ❤️ using Python & Streamlit. Feel free to fork, star ⭐, and connect with me on LinkedIn!
