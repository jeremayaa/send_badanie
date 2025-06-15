# 🧪 Send_Badanie – Django Web App for Medical Image Analysis

**Send_Badanie** is a simple Django-based web application designed to support medical laboratories by managing patients, surveys (medical image records), and analyses.

It includes a custom-built web-based program to create **binary masks for semantic segmentation** based on histopathological or other medical images.

It was developed as university project

---

## ✅ Features

- **User authentication** – login & registration for doctors
- **CRUD operations** for:
  - Patients
  - Surveys (medical images)
  - Analyses (manual or programmatic)
- **Canvas-based mask editor** (semantic segmentation)
- **Optional external analysis upload**
- REST API for dynamic frontend updates (AJAX via `fetch()`)
- Tag-based filtering & sorting for surveys

---

## 🖥️ Installation (macOS or Linux)

```bash
# Clone the repository
git clone https://github.com/jeremayaa/send_badanie.git
cd send_badanie

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App Locally

```bash
python manage.py runserver
```

Then open your browser and go to:  
`http://127.0.0.1:8000/`
