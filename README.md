# MOVIE RESERVATION SYSTEM

This backend system for a movie reservation service allows users to sign up, log in, browse movies, reserve seats for specific showtimes, and manage their reservations.

## Recent Improvements

- **Professional Permissions:** Implemented `AdminOrReadOnly` logic. Authenticated users can browse (GET), while only Admins can modify (POST/PUT/DELETE).
- **Refactored API:** Cleaned up `cinemas` views using idiomatic DRF patterns and robust error handling.
- **Smart Scheduling:** Modified `Showtime` model to use `DateTimeField` and implemented automatic overlap detection. The system now prevents scheduling two movies on the same screen at the same time.
- **Improved Data Integrity:** Changed `Movie.duration` to `PositiveIntegerField` (minutes) for precise end-time calculations.

## Goal

- To implement complex business logic like seat reservation and scheduling, focusing on data relationships and high-performance queries.

## API Documentation

### Authentication
- `POST /api/auth/signup/` - Register a new user.

### Movies
- `GET /api/movies/` - List all movies.
- `POST /api/movies/` - Add a movie (Admin only).
- `GET /api/movies/<id>/` - Get movie details.
- `PATCH /api/movies/<id>/` - Update movie (Admin only).

### Cinemas & Screens
- `GET /api/cinemas/` - List all cinemas.
- `POST /api/cinemas/` - Create a cinema (Admin only).
- `GET /api/cinemas/<id>/screens/` - List screens in a specific cinema.
- `POST /api/cinemas/<id>/screens/` - Add a screen to a cinema (Admin only).

### Showtimes
- `GET /api/showtimes/` - List all showtimes.
    - Query params: `movie_id`, `date` (YYYY-MM-DD).
- `POST /api/showtimes/` - Create a showtime (Admin only).
    - **Logic:** Automatically validates against overlaps on the same screen.
- `GET /api/showtimes/<id>/` - Get showtime details.

## Requirements Progress

### User Authentication and Authorization
- [x] Users should be able to sign up and log in.
- [x] Roles for users (Admin/User).
- [ ] Regular users should be able to reserve seats.

### Movie & Showtime Management
- [x] Admins can manage movies.
- [x] Admins can manage showtimes with scheduling logic.
- [x] Movies categorized by duration and title.
- [x] Users can filter showtimes by movie or date.

### Reservation Management (Next Steps)
- [ ] Implement `Booking` model.
- [ ] Implement seat availability logic.
- [ ] Prevent overbooking during reservation.

## Data Model

```markdown
# Movie
- id, title, description, duration (mins), poster

# Cinemas
- id, name, city, country, total_screen

# Screen
- id, cinema_id, screen_number, total_seats

# Showtime
- id, movie_id, screen_id, start_time, end_time (computed), status, base_price
```

## Implementation Notes
- **Overlap Detection:** The `Showtime.clean()` method ensures that `start_time` and `end_time` (start + duration) do not collide with existing shows on the same `screen_id`.
- **Permissions:** `AdminOrReadOnly` ensures data security while allowing public browsing.
