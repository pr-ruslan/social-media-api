# social-media-api
RESTful backend API for a social media platform built with Django and Django REST Framework.
Supports user authentication (JWT), profiles, posts, comments, likes, and follow relationships.

### Authentication

-   JWT-based authentication
-   Login → receive access & refresh tokens
-   Logout → token invalidation (blacklisting)
-   Protected endpoints for authenticated users

### User Profiles

-   Create profile (1-to-1 with User)
-   View own profile (`/profiles/me/`)
-   View other users' profiles
-   Update profile
-   Delete profile
-   Upload/replace profile logo
-   Search by email, first name, last name
-   Filter by gender

### Posts

-   Create / update / delete posts
-   Retrieve:
    -   Own posts
    -   Posts of followed users (feed)
    -   All posts
-   Filter posts by hashtags (normalized to lowercase)
-   Optimized querysets (`select_related`, `prefetch_related`)

### Likes

-   Like / Unlike posts
-   Retrieve posts liked by current user

### Comments

-   Add comments to posts
-   Retrieve comments for a post

### Following System

-   Follow / unfollow users
-   Retrieve feed of followed users' posts

------------------------------------------------------------------------

## Tech Stack

-   Python 3.x
-   Django
-   Django REST Framework
-   SQLite
-   SimpleJWT
-   Django Filter

------------------------------------------------------------------------

## Environment Variables (.env)

SECRET_KEY=your_secret_key\
DEBUG=True

------------------------------------------------------------------------

## Installation

``` bash
git clone https://github.com/your-username/social-network-api.git
cd social-network-api

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

------------------------------------------------------------------------

## Purpose

This project demonstrates:

-   REST API architecture design
-   Authentication & authorization
-   Custom permissions
-   Query optimization
-   Clean modular structure
-   Production-ready backend practices

------------------------------------------------------------------------

## License

MIT
