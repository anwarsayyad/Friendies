# Friendies

Friendies is a Django-based API for managing user friendships. It includes features for user authentication, searching for users, sending and responding to friend requests, and listing friends and pending requests.

## Features

- **User Authentication**: Basic authentication using username(email) and password to secure the API.
- **Search Users**:
  - Search by email or name.
  - If the search keyword matches the exact email, return the user associated with the email.
  - If the search keyword contains any part of the name, return a list of matching users.
- **Friend Requests**:
  - Send friend requests to other users.
  - Accept or reject received friend requests.
  - List all friends who have accepted the friend request.
  - List pending friend requests that have been received.
- **Rate Limiting**: Users cannot send more than 3 friend requests within a minute.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/anwarsayyad/Friendies.git
cd Friendies
```

2. **Build  Docker iamge**

```bash
docker-compose build
```

This command will:
- Build the Docker image for the Django app.

3. **Run docker or start container**

```bash
docker-compose up
```
This command will
- Start the PostgreSQL database container.
- Run the Django development server on `http://localhost:8000`.

4. **Run database migrations**

```bash
docker-compose run --rm app sh -c "python manage.py migrate"
```

5. **Create a superuser**

```bash
docker-compose run --rm app sh -c  "python manage.py createsuperuser"
```
## Usage

### API Endpoints

<!-- #### Authentication -->

<!-- - **Login:** `/api/token/` (POST)
- **Refresh Token:** `/api/token/refresh/` (POST) -->

#### User Management

- **Crate User:** `/api/user/create/` (POST)
      ```http
    GET /api/user/create/
    Authorization: Basic Authorization
    {
        "email": "user@example.com",
        "password": "string",
        "name": "string"
    }
    ```
- **Retrive Update API:** `/api/user/profile-setting/` (GET PUT PATCH)

- **Search Users:** `/api/friends/users/search/?search=keyword` (GET)

  **Example Requests:**

  - **Search by email:**

    ```http
    GET /api/friends/users/search/?search=example@example.com
    Authorization: Basic Authorization
    ```

  - **Search by name:**

    ```http
    GET /api/friends/users/search/?search=am
    Authorization: Basic Authorization
    ```

#### Friend Requests

- **Send Friend Request:** `/api/friends/friendship/send/` (POST)

  **Example Request:**

  ```http
  POST /api/friendship/send/
  Content-Type: application/json
  Authorization: Basic Authorization

  {
  "requests_to": {
    "name": "string",
    "email": "user@example.com"
  }
}
  ```

- **Respond to Friend Request:** `/api/friends/friendship/{id}/respond/` (POST)

  **Example Request:**

  ```http
  POST /api/friends/friendship/{id}/respond/
  Content-Type: application/json
  Authorization: Basic Authorization

  {
      "action": "accept"  # or "reject"
  }
  ```

- **List Friends:** `/api/friendship/` (GET)

  **Example Request:**

  ```http
  GET /api/frieds/friendship-accepted-list/
  Authorization: Basic Authorization
  ```

- **List Pending Friend Requests:** `/api/friends/friendship/pending/` (GET)

  **Example Request:**

  ```http
  GET /api/friedns/friendship/pending/
  Authorization: Basic Authorization
  ```

### Running Tests

To run the tests, use the following command:

```bash
docker-compose run --rm app sh -c "python manage.py test"
```

## API Documentation

Swagger UI is available at `http://localhost:8000/api/docs/` and schema `http://localhost:8000/api/schema/`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact [Anwar Sayyad](mailto:anwarsayyad2631@gmail.com).
```
