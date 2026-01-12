- uvicorn: lightweight, fast ASGI server for Python, commonly used to run asynchronous web applications, particularly with frameworks like FastAPI or Starlette
- fastapi route `/docs` : serves a Swagger UI web page
- pydantic: library for data validation and settings management using type annotations, ensuring that the data is conform to the types and rules defined
- sqlite: lightweight relational database
- sqlalchemy: ORM
- sqlmodel: built on pydantic and sqlalchemy, to enable one class to serve multiple purposes:
	- define a database table
	- validate incoming request data
	- serialize API responses
	- provide type hints everywhere
	(One class = API schema + DB table)
- readiness vs startup health concern
- `Depends()`: takes a single "dependable" callable (like a function) -> Declare a FastAPI dependencyI
- SQLModel (the class) inherits from pydantic's BaseModel and SQLAlchemy declarative base
- `Field(...)` is both:
	- a Pydantic validator (checks types at runtime)
	- a SQLAlchemy column definition (sets PK, default, index)

