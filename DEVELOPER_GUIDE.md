> **Note:** This document is a work-in-progress and will be updated as the project evolves.

# Naebak Ratings Service: Developer Guide

**Version:** 1.0.0  
**Last Updated:** September 26, 2025  
**Author:** Manus AI

---

## 1. Service Overview

The **Naebak Ratings Service** is responsible for managing user ratings and reviews for political candidates, representatives, and content on the Naebak platform. It provides a system for collecting, calculating, and displaying ratings to help users make informed decisions.

### **Key Features:**

-   **User Ratings:** Allows users to submit ratings on a scale of 1 to 5.
-   **Smart Rating Algorithm:** Calculates a weighted average rating based on user reputation and other factors.
-   **Rating History:** Stores all user ratings for auditing and analysis.
-   **API for Ratings:** Provides an API for other services to retrieve ratings.

### **Technology Stack:**

-   **Framework:** Django
-   **Database:** PostgreSQL
-   **API Documentation:** drf-spectacular (Swagger/OpenAPI)

---

## 2. Local Development Setup

### **Prerequisites:**

-   Python 3.11+
-   Poetry
-   PostgreSQL
-   Redis

### **Installation:**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/egyptofrance/naebak-ratings-service.git
    cd naebak-ratings-service
    ```

2.  **Install dependencies:**

    ```bash
    poetry install
    ```

3.  **Configure environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=postgres://user:password@localhost:5432/naebak_ratings
    REDIS_URL=redis://localhost:6379/0
    ```

4.  **Run database migrations:**

    ```bash
    poetry run python manage.py migrate
    ```

5.  **Start the development server:**

    ```bash
    poetry run python manage.py runserver
    ```

    The service will be available at `http://127.0.0.1:8000`.

---

## 3. Running Tests

To run the test suite, use the following command:

```bash
poetry run python manage.py test
```

---

## 4. API Documentation

The API documentation is automatically generated using `drf-spectacular` and is available at the following endpoints:

-   **/api/schema/**: OpenAPI 3.0 schema.
-   **/api/schema/swagger-ui/**: Swagger UI.
-   **/api/schema/redoc/**: ReDoc.

---

## 5. Deployment

The service is designed to be deployed as a containerized application using Docker and Google Cloud Run. A `Dockerfile` is provided for building the container image.

---

## 6. Dependencies

Key dependencies are listed in the `pyproject.toml` file. Use Poetry to manage dependencies.

---

## 7. Contribution Guidelines

Please follow the coding standards and pull request templates defined in the central documentation hub. All contributions must pass the test suite and include relevant documentation updates.
