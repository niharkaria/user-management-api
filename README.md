![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

🚀 FASTAPI | JWT AUTH | POSTGRESQL | USER MANAGEMENT

# User Management API

A RESTful API built with FastAPI for user management with JWT authentication. This project demonstrates core backend concepts including user registration, authentication, profile management, and database operations.

## Features

- ✅ User Registration with email and username uniqueness validation
- ✅ User Login with JWT token authentication
- ✅ Password hashing using bcrypt
- ✅ Protected routes with JWT middleware
- ✅ User profile retrieval and updates
- ✅ Account deactivation (soft delete)
- ✅ PostgreSQL database integration
- ✅ Input validation with Pydantic
- ✅ Interactive API documentation (Swagger UI)

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Passlib with bcrypt
- **Validation**: Pydantic

## Project Structure
```
user-management-api/
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy models (User table)
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Database CRUD operations
├── auth.py              # Authentication utilities (JWT, password hashing)
├── dependencies.py      # FastAPI dependencies
├── routes.py            # API endpoints
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/user-management-api.git
cd user-management-api
```

2. **Create virtual environment**
```bash
python -m venv myvenv
myvenv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create PostgreSQL database**
```sql
CREATE DATABASE user_management_db;
```

5. **Configure database connection**

Edit `config.py` and update the `DATABASE_URL`:
```python
DATABASE_URL: str = "postgresql://username:password@localhost:5432/user_management_db"
```

Replace `username` and `password` with your PostgreSQL credentials.

6. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register a new user |
| POST | `/api/login` | Login and get access token |

### Protected Endpoints (Requires Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile` | Get current user profile |
| PUT | `/api/profile` | Update user profile |
| DELETE | `/api/profile` | Deactivate user account |

## Usage Examples

### 1. Register a new user
```bash
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST "http://127.0.0.1:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Profile (Protected)
```bash
curl -X GET "http://127.0.0.1:8000/api/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Update Profile (Protected)
```bash
curl -X PUT "http://127.0.0.1:8000/api/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated"
  }'
```

## Configuration

Key configuration settings in `config.py`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token signing (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)

## Security Features

- Passwords are hashed using bcrypt before storage
- JWT tokens for stateless authentication
- Email and username uniqueness validation
- Protected routes require valid JWT token
- Soft delete for user accounts (preserves data)

## Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| email | String | Unique, Not Null |
| username | String | Unique, Not Null |
| hashed_password | String | Not Null |
| full_name | String | Nullable |
| is_active | Boolean | Default: True |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Learning Outcomes

This project covers:

- ✅ FastAPI framework basics
- ✅ RESTful API design
- ✅ Database modeling with SQLAlchemy
- ✅ JWT authentication implementation
- ✅ Password hashing and security
- ✅ Input validation with Pydantic
- ✅ CRUD operations
- ✅ Error handling
- ✅ API documentation

## Future Enhancements

🔐 Email verification
🔄 Refresh tokens
📸 Profile picture upload
👥 Role-based access control (RBAC)
🔄 Pagination for user list
📧 Password reset (OTP or email link)
🧪 Unit + Integration tests
🚫 Rate limiting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Contact
Nihar Karia  
📧 Email: niharkaria7@gmail.com  
🔗 GitHub: https://github.com/niharkaria