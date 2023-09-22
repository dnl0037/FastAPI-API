# FastAPI Social Media API

A FastAPI-based API for a social media platform with features like user authentication, post creation, and voting on posts. It utilizes PostgreSQL for data storage, Alembic for database migrations, and includes unit tests with pytest. The application can be deployed on Heroku, Docker, and an Ubuntu server, with continuous integration and continuous deployment (CI/CD) pipelines.


## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Testing](#testing)
- [Deployment](#deployment)
- [CI/CD Pipeline](#ci/cd-pipeline)
- [Contribution](#contribution)


## Requirements

Make sure you have the following requirements installed:

- Python 3.9
- PostgreSQL 
- Postman


## Installation

1. Clone this repository: 
    https://github.com/dnl0037/FastAPI-API.git
   
3. Create a virtual environment and activate it:
   ```bash
    python -m venv venv
    source venv/bin/activate
    On Windows: venv\Scripts\activate
5. Install the dependencies:
   ```bash
    pip install -r requirements.txt  
7. Configure environment variables (e.g., in a `.env` file): You will need to set this variables according to your database.
    - DB_USERNAME=
    - DB_HOSTNAME=
    - DB_PORT=
    - DB_PASSWORD=
    - DB_NAME=
    - SECRET_KEY= *This is required to create a Token for user authentication* Check the file app/oauth2.py
    - ALGORITHM= *This is required to create a Token for user authentication* 
    - TOKEN_EXPIRATION_TIME= *This is required to create a Token for user authentication*
      
8. Apply database migrations:
   ```bash
   alembic upgrade head
10. Run the application locally:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
12. The application will be available at `http://localhost:8000`.



## Usage with Postman

### 1. Create a User

- To use the application, first, create a user.

- Open Postman and create a new request.

- Configure the request to make a POST request to your application's URL, for example: `http://localhost:8000/users/` if you are running it locally.

- In the request body, add user data in JSON format. For example:

  ```json
  {
      "email": "example@example.com",
      "password": "password123"
  }
- Click "Send" to send the request. This will create a new user in the database.

### 2. Log In (Obtain a Token)

- After creating a user, you can proceed to log in.
  
- Configure a new request to make a POST request to the login endpoint, for example: http://localhost:8000/login.
  
- In the request body, use the OAuth2PasswordRequestForm format to provide login credentials:
  ```json
  {
      "username": "example@example.com",
      "password": "password123"
  }
- Click "Send" to send the request. This will return an access token.

### 3. Use the Access Token

- To access protected endpoints, you need to include the access token in the Authorization header of your requests. On Postman, click on `Authorization`, select `Bearer token` and paste your token.

- Create a new request to access an endpoint that requires authentication, such as creating a post:

- Configure the request with the appropriate method (e.g., POST).

- Set the request URL to the endpoint you want to access (e.g., http://localhost:8000/posts/).

- In the request body, provide the post data in JSON format:
  ```json
  {
      "title": "My First Post",
      "content": "Hi, this is my first post."
  }
  
- Click "Send" to send the request. This will create a new post with the provided data
  ```json
  {
      "title": "My First Post",
      "content": "Hi, this is my first post.",
      "published": true,
      "id": 1,
      "created_at": "2023-09-22T10:56:02.919752-06:00",
      "user_id": 1,
      "user": {
          "id": 1,
          "email": "example@example.com"
      }
  }
  
### 4. Voting 

- Set the request URL to the endpoint http://localhost:8000/votes/
  
- In the request body, provide the vote data in JSON format:
  ```json
  {
      "post_id" : 1,
      "vote_dir" : 1   # 1 to upvote and 0 to downvote
  }

- Check out the rest of the [endpoints](#api-endpoints)



## Project Structure

The most important folders in this project are:

- `app`: This folder contains the following Python files: `config.py`, `database.py`, `main.py`, `models.py`, `oauth2.py`, `schemas.py`, and `utils.py`.

  - In addition, there's a subfolder named `routers` with `login.py`, `users.py`, `votes.py`, and `posts.py`. Each of these routers handles specific API endpoints.

  - `config.py` defines application settings using the `Settings` class.

  - `database.py`: This file configures the database connection and session handling using SQLAlchemy.

  - `models.py`: This file defines the data models for the application, including `Post`, `User`, and `Votes`.

  - `oauth2.py`: This file contains OAuth2 authentication settings, including `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE`.

  - `schemas.py`: This file defines Pydantic models used for request and response payloads.

  - `utils.py`: This file contains utility functions, such as password hashing and validation.

- `tests`: This folder contains unit tests for the application.

  - Inside this folder, you will find various test files that cover different aspects of the application's functionality.



## API Endpoints

### Users

- `POST /users/`: Create a new user.
- `GET /users/{id}`: Get user details by ID.
- 
### Authentication

- `POST /login`: Log in and obtain an access token.

### Posts

- `GET /posts/`: Get a list of posts.
- `POST /posts/`: Create a new post.
- `GET /posts/{id}`: Get post details by ID.
- `PUT /posts/{id}`: Update an existing post.
- `DELETE /posts/{id}`: Delete a post.

### Voting

- `POST /votes/`: Vote for a post.

## Data Models

### `Post` Model

- The `Post` model represents individual posts in your social media application.

- It has the following attributes:
  - `id`: An auto-incrementing integer serving as the primary key.
  - `title`: A string field for the title of the post.
  - `content`: A string field for the content of the post.
  - `published`: A boolean field indicating whether the post is published.
  - `created_at`: A timestamp field indicating when the post was created.
  - `user_id`: An integer field representing the ID of the user who created the post.

- There is a relationship defined with the `User` model using the `user_id` field, indicating that each post is associated with a user.

### `User` Model

- The `User` model represents users of your social media application.

- It has the following attributes:
  - `id`: An auto-incrementing integer serving as the primary key.
  - `email`: A string field for the email address of the user. It is also marked as unique to ensure email uniqueness.
  - `password`: A string field for the hashed password of the user.
  - `created_at`: A timestamp field indicating when the user account was created.

- The `User` model is related to the `Post` model through the `user_id` field, establishing that a user can create multiple posts.

### `Votes` Model

- The `Votes` model represents votes or likes on posts in your application.

- It has two primary key fields:
  - `user_id`: An integer field representing the ID of the user who voted.
  - `post_id`: An integer field representing the ID of the post that received the vote.

- These two fields together form a composite primary key, ensuring that each user can vote on a post only once.

- The `ondelete="CASCADE"` option in the foreign key constraints indicates that when a user or post is deleted, their corresponding votes should also be deleted.

**Example of relationships:**
- A `User` can create multiple `Post` objects.
- A `Post` can have multiple `Votes` from different `User` objects.

These data models define the core structure of the application, allowing users to create posts, vote on posts, and maintain user accounts.



## Testing

To run unit tests using pytest:

1. Make sure you have pytest installed. If not, you can install it using pip:

   ```bash
   pip install pytest

2. Navigate to the root directory of your project in your terminal.

3. Run the following command to execute all unit tests:

   ```bash
   pytest
   ```


## Deployment

### Heroku

- After installing, logging set your Heroku account, you can use the  `Procfile` from this repository. You will also need to set up a `Heroku Postgres` add-on and configure your database credentials accordingly. 

### Ubuntu DigitalOcean

-  This repository contains the `gunicorn.service` and `nginx` files you will need to launch the app after you are done setting up your machine.

### Docker

- This repository contains 3 files: `Dockerfile`, `docker-compose-dev.yml` and `docker-compose-prod.yml` with the necessary instructions to create your image and run your container.



## CI/CD pipeline


This configuration `.github/workflows/build-deploy.yml` file defines a Continuous Integration/Continuous Deployment (CI/CD) pipeline that automates the build, test, and deployment of the application. It ensures your project runs smoothly in different environments and updates automatically when changes are made to your repository.

### Description

This pipeline file runs every time a `push` or `pull request` is made to the repository. The pipeline is divided into two main jobs:

#### `build` (Build)

This job is responsible for building and testing the application. Here's a detailed description of the actions it performs:

1. **Environment Setup:** Necessary environment variables for the application, such as database credentials and secret keys, are set.

2. **PostgreSQL Service:** A PostgreSQL container is started for database testing.

3. **Environment Preparation:**

   - **Checkout Git Repository:** The codebase is fetched from the repository.

   - **Install Python 3.9:** Python 3.9 is set up for the environment.

   - **Upgrade Pip:** Pip is upgraded to the latest version.

   - **Install Dependencies:** Required dependencies specified in `requirements.txt` are installed.

   - **Run Tests with Pytest:** The application is tested using Pytest.

   - **Docker Image Build and Push:** 

   - **Login to Docker Hub:** 

   - The pipeline logs in to Docker Hub using credentials from secrets. 

   - **Set up Docker Buildx:** 

   - Docker Buildx is set up for building and pushing images. 

   - **Build and Push Docker Image:** 

   - The Docker image is built and pushed to the Docker Hub registry. 

   - You can specify image tags and caching options in this section. 

   - **Image Digest:** 

   - The image digest is displayed in the pipeline output.

#### `deploy`

This job runs on an Ubuntu-based environment and deploys the application. It depends on the `build` job to complete successfully. Here's a description of the actions it performs:

1. **Environment Preparation:**

   - **Checkout Git Repository:** The codebase is fetched from the repository.

   - **Deploy to Heroku:** The application is deployed to Heroku using the `akhileshns/heroku-deploy` action. Heroku API key, app name, and email are provided from secrets.

   - **Deploy to Ubuntu Server:** The application is deployed to an Ubuntu server using the `appleboy/ssh-action`. SSH credentials and deployment script are provided from secrets.

This CI/CD pipeline ensures that your application is built, tested, and deployed automatically, reducing manual intervention and ensuring a streamlined development process.



## Contribution

If you want to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch for your contribution.
3. Make your changes and create a pull request.


