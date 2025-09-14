# NPC Generator API (Django + Gemini AI)

**NPC Generator API** an app powered by Gemini AI that creates and manages rich,
story-driven non-player characters (NPCs) from narrative prompts.

---

## 📋 Main Requirements

- Python 3.10
- Django 5.2
- djangorestframework 3.16.0
- google-genai

---

## 🛠️ Local installation

### 1. Prepare the environment

```bash
mkdir NPC_Generator_API
cd NPC_Generator_API
git clone https://github.com/marcin86junior/?.git .
cd NPC_Generator_API
python -m venv .venv
```

### 2. Activate the environment
- **Windows (PowerShell)**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the environment
Copy the `.env.template` file to '.env' in main folder and fill in the appropriate data:
GEMINI_API_KEY

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Add story to db
```bash
python manage.py shell -c "from npc_api.models import Story; Story.objects.create(title='The Chronicles of the Sundered Realm', content=open('data/fantasy.md').read())"
```
or
```bash
http://127.0.0.1:8000/swagger/
POST /stories/
title: The Chronicles of the Sundered Realm
data from "data/fantasy.md"
```

or 
```bash
django-admin -> add story via admin panel
```

### 7. Create a superuser (not required)
```bash
python manage.py createsuperuser
```

### 8. Run the server
```bash
python manage.py runserver
http://127.0.0.1:8000/swagger/
```

### 9. How to run test it?
Go to `npc_api/tests` and fill the `GEMINI_API_KEY` in `test_settings.py`

### 10. Run test
```bash
python manage.py test
```

---

## 🐳 Run via Docker
### 1. Build the image
```bash
docker-compose up -d --build
```
### 2. Run the container
```bash
docker-compose up
```

---

## 🌐 Avaiable adresses
- App: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/
