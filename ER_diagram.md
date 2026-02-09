```mermaid
erDiagram
    USERS {
        UUID id PK
        string email
        string hashed_password
        string full_name
        string phone_number
        boolean is_admin
    }

    TABLES {
        int id PK
        string name
        int capacity
    }

    BOOKINGS {
        UUID id PK
        UUID user_id FK
        int table_id FK
        datetime booking_start
        datetime booking_end
    }

    USERS ||--o{ BOOKINGS : "has"
    TABLES ||--o{ BOOKINGS : "is booked in"