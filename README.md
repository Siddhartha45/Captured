[captured-README.md](https://github.com/user-attachments/files/26529128/captured-README.md)
# Captured 📷

A photo journaling web app where users can upload and share their trek and travel photos with personal descriptions. Built as a personal project to document my trekking experiences across Nepal.

🔗 **Live Demo:** [captured.onrender.com](https://captured.onrender.com)

---

## Features

- User registration and authentication (sign up / sign in)
- Upload photos with a title and personal description
- User can edit and delete their photos
- Photos stored and served via Cloudinary CDN
- Public gallery — anyone can browse uploaded photos
- Deployed on Render with PostgreSQL as the production database

---

## Tech Stack

| Layer      | Technology                                            |
|------------|-------------------------------------------------------|
| Backend    | Python 3, Django 5.2                                  |
| Database   | PostgreSQL (production), SQLite (development)         |
| Storage    | Cloudinary (image hosting & CDN)                      |
| Deployment | Render                                                |

---

## Project Structure

```
Captured/
├── captured/        # Core app — photo models, views, URLs
├── user/            # Auth app — registration, login, profile
├── config/          # Django project settings
├── templates/       # HTML templates
├── static/          # CSS, JS, static assets
└── requirements.txt
```

---
