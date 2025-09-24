# Masterblog API
Masterblog is a Flask-based blog application. The frontend uses Flask templates combined with JavaScript for dynamic interactions, while the backend provides a RESTful API for managing posts. Swagger UI is included for easy API exploration

## Features

- **List Posts**: Retrieve all posts with optional sorting and pagination.
- **Create Post**: Add a new post with a title and content.
- **Update Post**: Edit an existing post by ID.
- **Delete Post**: Remove a post by ID.
- **Search Posts**: Search posts by title or content.
- **Swagger UI**: Interactive API documentation available at `/api/docs`.

## Future Features

1. **Expand Data Model**: Include more complex features like comments, categories, or tags for posts.
2. **User Authorization**: Add user registration and login endpoints, allowing only authenticated users to create, update, or delete posts.

## Getting Started

1. Clone the repository:

```bash
git clone <your-repo-url>
cd masterblog
```

## Install dependencies
pip install -r requirements.txt

## Run the backend:
python backend/backend_app.py

## Open Swagger UI in your browser:
http://localhost:5002/api/docs

