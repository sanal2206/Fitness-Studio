# 🏋️‍♂️ Fitness Studio Booking API

A Django REST Framework API for managing fitness classes and bookings. Clients can view classes, book spots, and see their bookings using their email. Timezone support ensures bookings are shown in the user's preferred timezone.

---

##  Features

- View all upcoming fitness classes (Yoga, Zumba, HIIT, etc.)
- Book a class if slots are available
- List all bookings by email address
- Timezone-aware: classes created in IST, bookings viewable in user’s local timezone
- Input validation and error handling
- Seed data for easy testing
- Django REST Framework for powerful API development

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sanal2206/Fitness-Studio.git
cd Fitness-Studio
```

### 2. Create & Activate a Virtual Environment

```bash
python3 -m venv venv
# Activate on Linux/macOS
source venv/bin/activate
# OR Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Seed Sample Data

```bash
python manage.py seed_data
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

##  API Documentation

Postman collection for sample requests:  
[Fitness Studio Booking API Postman Collection](https://www.postman.com/cryosat-administrator-93474914/workspace/fitness-studio/collection/39810980-e990dc07-6bd7-431e-96d7-7d6e65a6a1d4?action=share&creator=39810980)

### Endpoints

#### 1. List Classes

```
GET /api/classes/
```
_Response:_
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-10 08:30:00 IST",
    "instructor": "Alice",
    "available_slots": 10
  }
]
```

#### 2. Book a Class

```
POST /api/book/
```
_Body (JSON):_
```json
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```
_Possible errors:_
- Invalid email format
- Class does not exist
- No available slots
- Missing fields

#### 3. List Bookings by Email

```
GET /api/bookings/?email=john@example.com
```
_Response:_
```json
[
  {
    "fitness_class": {
      "id": 1,
      "name": "Yoga",
      "datetime": "2025-06-10 08:30:00 IST",
      "instructor": "Alice",
      "available_slots": 10
    },
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "booked_at": "2025-06-02 12:26:00 IST"
  }
]
```

---

##  Timezone Handling

- All class times are stored in IST (Asia/Kolkata).
- Bookings and listings can be displayed in user’s local timezone (pass `timezone` as a query param, e.g. `?timezone=America/New_York`).

---

##  Testing
 
- Use the provided Postman collection for manual API testing.

---

##  Seed Data

- Use `python manage.py seed_data` to load sample classes for demo/testing.

---

##  Error Handling

- Graceful responses for overbooking, invalid input, and missing fields.
- Proper HTTP status codes and error messages.

---

##  Author

- [Sanal S](https://github.com/sanal2206)

---

 
