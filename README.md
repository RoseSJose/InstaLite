# InstaLite

InstaLite is a lightweight, full-stack web application inspired by Instagram. It features a Python Flask backend and a modern frontend, designed for learning, prototyping, or as a foundation for social media projects.

## Features
- User registration and login (JWT authentication)
- Profile page with follower/following counts and user posts
- Image upload and feed display
- Follow/unfollow other users
- Like/unlike posts
- Comment on posts
- Delete your own posts
- Responsive UI with Streamlit (supports dark mode)

## Project Structure
```
InstaLite/
│
├── backend/
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── utils/
│       └── auth_utils.py
│
├── frontend/
│   └── (frontend code)
│
├── .gitignore
└── README.md
```

## Getting Started

## API Overview

| Method | Endpoint                | Description                                      |
|--------|-------------------------|--------------------------------------------------|
| POST   | /register               | Register a new user (username, email, password)  |
| POST   | /login                  | Login and receive a JWT token                    |
| GET    | /profile                | Get current user's profile, posts, followers, and following |
| GET    | /followers/&lt;user_id&gt;   | List user IDs of followers                       |
| GET    | /following/&lt;user_id&gt;   | List user IDs the user is following              |
| POST   | /upload_post            | Upload a new post (image, caption)               |
| DELETE | /delete_post/&lt;post_id&gt; | Delete a post by ID                              |
| GET    | /feed                   | Get feed of posts from followed users and self   |
| POST   | /follow                 | Follow a user (provide user_id)                  |
| POST   | /unfollow               | Unfollow a user (provide user_id)                |
| POST   | /like                   | Like or unlike a post (toggle, provide post_id)  |
| GET    | /likes/&lt;post_id&gt;        | Get like count for a post                        |
| POST   | /comment                | Add a comment to a post (post_id, text)          |
| GET    | /comments/&lt;post_id&gt;     | Get all comments for a post                      |

### Backend Setup
1. Navigate to the backend directory:
	```
	cd backend
	```
2. (Optional) Create and activate a virtual environment:
	- On Windows:
	  ```
	  python -m venv venv
	  venv\Scripts\activate
	  ```
	- On macOS/Linux:
	  ```
	  python3 -m venv venv
	  source venv/bin/activate
	  ```
3. Install dependencies:
	```
	pip install -r requirements.txt
	```
4. Run the Flask app:
	```
	python app.py
	```

### Frontend Setup
- Run the following commands
```
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.