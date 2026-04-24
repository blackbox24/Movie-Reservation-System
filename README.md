# MOVIE RESERVATION SYSTEM

https://roadmap.sh/projects/movie-reservation-system

This backend system for a movie reservation service allows users to sign up, log in, browse movies, reserve seats for specific showtimes, and manage their reservations.

## Recent Improvements

- **Booking System:** Implemented a full reservation system with seat-level validation.
- **Seat Safety:** Uses database transactions and specific seat checks (`seat_row`, `seat_number`) to prevent double-booking.
- **Auto-Calculations:** Total price is automatically calculated based on showtime base price and ticket count.
- **Smart Scheduling:** Modified `Showtime` model to use `DateTimeField` and implemented automatic overlap detection.
- **Professional Permissions:** Refactored all apps to use consistent, secure DRF patterns.

## Goal

- To implement complex business logic like seat reservation and scheduling, focusing on data relationships and high-performance queries.

## API Documentation

### Authentication
- `POST /api/auth/signup/` - Register a new user.

### Movies & Showtimes
- `GET /api/movies/` - List all movies.
- `GET /api/showtimes/` - List all showtimes.
    - Query params: `movie_id`, `date` (YYYY-MM-DD).
- `GET /api/showtimes/<id>/` - Get showtime details (includes `remaining_seats`).

### Bookings (New)
- `GET /api/bookings/` - List your bookings (Admins see all).
- `POST /api/bookings/` - Create a reservation.
    - **Payload:** `{"showtime": id, "tickets": [{"seat_row": "A", "seat_number": 1}, ...]}`
    - **Logic:** Validates seat availability and future date. Uses Atomic transactions.
- `GET /api/bookings/<id>/` - Get booking details and tickets.
- `PATCH /api/bookings/<id>/cancel/` - Cancel an upcoming reservation.

## Requirements Progress

### User Authentication and Authorization
- [x] Users should be able to sign up and log in.
- [x] Roles for users (Admin/User).
- [x] Regular users can reserve seats.

### Movie & Showtime Management
- [x] Admins can manage movies.
- [x] Admins can manage showtimes with scheduling logic.
- [x] Users can filter showtimes by movie or date.

### Reservation Management
- [x] Implement `Booking` and `Ticket` models.
- [x] Implement seat selection logic.
- [x] Prevent overbooking and double-booking seats.
- [x] Users can see and cancel their upcoming reservations.

## Data Model

```markdown
# Movie
- id, title, description, duration (mins)

# Showtime
- id, movie_id, screen_id, start_time, end_time (computed), base_price

# Booking
- id, user_id, showtime_id, total_amount, status, created_at

# Ticket
- id, booking_id, seat_row, seat_number
```

## Implementation Notes
- **Atomic Bookings:** The booking process is wrapped in a transaction. If a seat becomes unavailable during the request, the entire booking is rolled back.
- **Remaining Seats:** `Showtime` has a dynamic property `remaining_seats` that calculates availability in real-time.
- **Cancellation Policy:** Bookings can only be cancelled *before* the showtime starts.
