# HBnB Evolution Application

In Part 2 of the HBnB Evolution project, you will enhance your application by integrating a relational database using SQLAlchemy, an Object-Relational Mapper (ORM), and by implementing security measures through JWT authentication. 

- Understanding and Implementing ORM: How to Integrate SQLAlchemy into a Flask Application to Handle Database Operations Smoothly.

- Database Management: The configuration and management of a relational database, including schema design and migrations.

- Security implementation: Secure API endpoints using JWT authentication, ensuring data access is regulated and secure.

- Adaptability and scalability: Improve application adaptability by enabling dynamic switching between different persistence methods and preparing for scalable deployment.

## Project Structure


### Models

- **BaseModel**: Abstract class defining common attributes and methods.
- **City**: Represents a city.
- **Country**: Represents a country.
- **DataManager**: Manages data persistence.
- **Review**: Represents a review.
- **Place**: Represents a place.
- **User**: Represents a user.

### Endpoints

#### Users
- **POST /users**: Create a new user.
- **GET /users**: Retrieve a list of all users.
- **GET /users/{user_id}**: Retrieve details of a specific user.
- **PUT /users/{user_id}**: Update an existing user.
- **DELETE /users/{user_id}**: Delete a user.

#### Cities
- **POST /cities**: Create a new city.
- **GET /cities**: Retrieve a list of all cities.
- **GET /cities/{city_id}**: Retrieve details of a specific city.
- **PUT /cities/{city_id}**: Update an existing city.
- **DELETE /cities/{city_id}**: Delete a city.

#### Reviews
- **POST /places/{place_id}/reviews**: Create a new review for a specific place.
- **GET /users/{user_id}/reviews**: Retrieve all reviews written by a specific user.
- **GET /places/{place_id}/reviews**: Retrieve all reviews for a specific place.
- **GET /reviews/{review_id}**: Retrieve details of a specific review.
- **PUT /reviews/{review_id}**: Update an existing review.
- **DELETE /reviews/{review_id}**: Delete a review.

#### Amenities
- **POST /amenities**: Create a new amenity.
- **GET /amenities**: Retrieve a list of all amenities.
- **GET /amenities/{amenity_id}**: Retrieve details of a specific amenity.
- **PUT /amenities/{amenity_id}**: Update an existing amenity.
- **DELETE /amenities/{amenity_id}**: Delete an amenity.

#### app
##### get every endpoint from a flask image
- *app.register_blueprint(user_bp)
- *app.register_blueprint(country_city_bp)
- *app.register_blueprint(amenity_bp)
- *app.register_blueprint(place_bp)
- *app.register_blueprint(review_bp)



## FileTests

### UserTests

File: `tests/test_user.py`

### CityTests

File: `tests/test_country_city.py`

### ReviewTests

File: `tests/test_review.py`

### AmenityTests

File: `tests/test_amenity.py`

## Dockerization

## Pull the Docker Image
- MySQL

```sh
docker pull mysql
```

## Run the Database in a Docker Container
- MySQL

```sh
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
```

### `Dockerfile`

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV DEVELOPMENT=1

# Install dependencies
RUN apk update && \
	apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev && \
	rm -rf /var/cache/apk/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first for caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5000 for the application
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]


```

### Verification

To verify that your application is working correctly, open a web browser and navigate to `http://127.0.0.1:5000/`. You can also use tools like `curl` or Postman to make requests to your endpoints and verify that they are responding correctly.

#### Example `curl` command

```sh
curl http://127.0.0.1:5000/
```
## BUGS

N/A

## Author
Glorisabel Rivera Rodriguez
---