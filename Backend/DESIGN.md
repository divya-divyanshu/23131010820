# URL Shortener Microservice Design Document

## Overview
This document outlines the design of a URL Shortener Microservice built using Flask and SQLite.

## Technology Stack
- **Python**: Programming language used for backend development.
- **Flask**: Framework for building the microservice.
- **SQLite**: Lightweight database for storing URLs and their metadata.
- **SQLAlchemy**: ORM for database interactions.
- **Logging**: For tracking requests and errors.

## Database Schema
### URLMapping
- `id`: Integer, primary key.
- `original_url`: String, the long URL to be shortened.
- `short_code`: String, unique identifier for the shortened URL.
- `expiry`: DateTime, the expiration time of the shortened URL.

## API Endpoints
1. **Create Short URL**
   - **Method**: POST
   - **Route**: `/shorturls`
   - **Request Body**: JSON containing `url`, `validity`, and `shortcode`.
   - **Response**: JSON containing `shortLink` and `expiry`.

2. **Redirect**
   - **Method**: GET
   - **Route**: `/<shortcode>`
   - **Functionality**: Redirects to the original long URL if not expired.

3. **Get Stats**
   - **Method**: GET
   - **Route**: `/shorturls/<shortcode>`
   - **Response**: JSON containing URL statistics.

## Flow
1. User sends a POST request to `/shorturls` with the long URL.
2. The service generates a unique shortcode or uses a provided one.
3. The service stores the mapping in the database with an expiry time.
4. When the user accesses the shortened URL, the service checks if it is expired and redirects accordingly.
5. Users can retrieve statistics about the shortened URL.

## Conclusion
This design provides a simple yet effective way to shorten URLs and track their usage.