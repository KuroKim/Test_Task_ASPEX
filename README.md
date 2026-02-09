# Restaurant Booking System

A backend API for managing restaurant table reservations. The system handles user authentication, table availability checking, and booking creation with background email notifications.

Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy (Async)**, **Redis**, and **Celery**.

## 🚀 Features

- **User Authentication**: JWT-based registration and login.
- **Table Management**: Dynamic check for available tables avoiding double-booking.
- **Business Logic**: Enforces restaurant opening hours (12:00 - 22:00) and fixed 2-hour slots.
- **Background Tasks**: Asynchronous email notifications using Celery + Redis.
- **Containerization**: Fully Dockerized environment.

## 🛠 Tech Stack

- **Language**: Python 3.10
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (Async)
- **Broker**: Redis 7
- **Worker**: Celery
- **Migrations**: Alembic

## ⚡️ Quick Start

The project is configured to run with a single command.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KuroKim/Test_Task_ASPEX
   cd Test_Task_ASPEX
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   *Note: The application will automatically initialize the database and create default tables.*

3. **Access the API:**
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **API Schema**: [http://127.0.0.1:8000/api/v1/openapi.json](http://127.0.0.1:8000/api/v1/openapi.json)

## 🧪 Testing the API

1. **Register**: POST `/api/v1/auth/register`
2. **Login**: Click "Authorize" button and enter credentials.
3. **Check Availability**: GET `/api/v1/bookings/tables/available`
4. **Book a Table**: POST `/api/v1/bookings/`

## 📂 Project Structure

- `app/api`: API route handlers.
- `app/core`: Configuration and security settings.
- `app/db`: Database session and migrations.
- `app/models`: SQLAlchemy database models.
- `app/schemas`: Pydantic data schemas.
- `app/services`: Business logic layer.
- `app/worker`: Celery tasks and configuration.
