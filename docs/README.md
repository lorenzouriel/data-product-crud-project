# The Backend
Our backend will be an API, **which will be responsible for communicating between our frontend and the database.** Let's detail each of the folders and files in our backend.

### Fast API
FastAPI is a **web framework for building APIs with Python.** It is based on Starlette, which is an asynchronous framework for building APIs. 

### Uvicorn
Uvicorn is an **asynchronous web server, which is based on ASGI, which is a design for asynchronous web servers.** Uvicorn is the web server recommended by FastAPI, and it is the server we will use in this project.

### SQLAlchemy
SQLAlchemy is a **library for communicating with the database.** It is an **ORM (Object Relational Mapper)**, which is an object-relational mapping technique that **allows you to communicate with the database using objects.**

One of the main advantages of working with SQLAlchemy is that it is **compatible with various databases, such as MySQL, PostgreSQL, SQLite, Oracle, Microsoft SQL Server, Firebird, Sybase and even Microsoft Access.**

Furthermore, it performs data hygiene, preventing SQL Injection attacks.

### Pydantic
Pydantic is a **library for performing data validation.** It is used by FastAPI to **validate the data that is received by the API, and also to define the types of data that are returned by the API.**

## `docker-compose.yml`
This `docker-compose.yml` file defines an application composed of three services: `postgres`, `backend` and `frontend`, and creates a network called `mynetwork`. I will explain each part in detail:

### Postgres:
- `image`: `postgres:latest`: This service uses the latest PostgreSQL image available on Docker Hub.
- `volumes`: Maps the `/var/lib/postgresql/data` directory within the PostgreSQL container to a volume called `postgres_data` on the host system. This **allows database data to persist even when the container is shut down.**
- `environment`: Defines environment **variables to configure the PostgreSQL database**, such as database name (`POSTGRES_DB`), user name (`POSTGRES_USER`), and password (`POSTGRES_PASSWORD`).
- `networks`: Defines that this service is on the network called `mynetwork`.

### Backend:
- `build`: Specifies that Docker should build an image for this service, **using a Dockerfile located in the ./backend directory.**
- `volumes`: **Maps the `./backend` directory (on the host system) to the `/app` directory inside the container.** This allows changes to the backend source code to be reflected in the container in real time.
- `environment`: Defines the `DATABASE_URL` environment variable, **which specifies the URL to connect to the PostgreSQL database.**
- `ports`: **Maps port 8000 of the host system to port 8000 of the container**, allowing the service to be accessed through port 8000.
- `depends_on`: Indicates that this **service depends on the postgres service, ensuring that the database is ready before the backend is started.**
- `networks`: Also defines that **this service is on the `mynetwork` network.**

### Frontend:
- `build`: Similar to the backend, it specifies that Docker must build an image for this service, using a Dockerfile located in the `./frontend` directory.
- `volumes`: Maps the **`./frontend` directory (on the host system) to the `/app` directory inside the container, allowing for real-time changes.**
- `ports`: Maps port 8501 of the host system to port 8501 of the container, allowing access to the frontend through port 8501.
- `networks`: Defines that this service is also on the `mynetwork` network.

### Networks:
`mynetwork`: Defines a custom network for services to communicate with each other.

### Volumes:
`postgres_data`: Defines a volume to store PostgreSQL database data.

### `docker-compose` up command:
When you run `docker-compose up`, **Docker Compose will read the `docker-compose.yml` file, create the services as per the specified definitions, and start them.** 

This means that containers for the PostgreSQL database, backend and frontend will be created and connected to the `mynetwork` network. 

The database will be configured with the provided details (database name, user and password), and the images for the backend and frontend services will be built from the provided Dockerfiles. 

Once launched, you will be able to access the backend through `http://localhost:8000` and the frontend through `http://localhost:8501`. Database data will be persisted on the `postgres_data`volume.

```
├── backend
│   ├── Dockerfile # Config Docker file
│   ├── crud.py # CRUD functions using SQL Alchemy
│   ├── database.py # Database configuration file using SQL Alchemy
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── router.py
│   └── schemas.py
```

## `database.py` file
The `database.py` file is **responsible for configuring the database using SQLAlchemy.** It is responsible for creating the **connection to the database**, and also for **creating the database session.**

**If you want to change databases, you just need to change the connection URL, which is in the SQLALCHEMY_DATABASE_URL variable.** SQLAlchemy is compatible with various databases such as MySQL, PostgreSQL, SQLite, Oracle, Microsoft SQL Server, Firebird, Sybase and even Microsoft Access.

The main points of this file are the engine, which is the connection to the database, and the SessionLocal, which is the database session. **The SessionLocal is the one that executes the queries in the database.**

**Always remember to:**
1. Declare the bank URL
2. Create the engine using 'create_engine'
3. Create the bank session
4. Create the ORM Base (our Model will inherit it)
5. Create a session generator to be reused

## `models.py` file
The `models.py` file is responsible for **defining SQLAlchemy models, which are the classes that define the database tables. These models are used to communicate with the database.**

This is **where we define the table name, fields and data types.** We were able to include randomly generated fields, such as id and created_at. 

For the `id`, when including the Integer field, with the `primary_key=True` parameter, **SQLAlchemy already understands that this field is the table's id.** For `created_at`, when including the **DateTime field, with the `default=datetime` parameter, SQLAlchemy already understands that this field is the table's creation date.**

**To remember:**
1. The models are bank agnostic, they don't know which bank is created! It will import the database base!
2. Declare your Table

## `schemas.py` file
The `schemas.py` file is **responsible for defining Pydantic's schemas, which are the classes that define the types of data that will be used in the API.** 
-   These schemas are **used to validate the data received by the API, and also to define the types of data that are returned by the API.**

**One dvantage is its pre-defined types, which make our lives a lot easier.** For example, if you want to define a field that only accepts positive numbers, you can use `PositiveInt`. If you want to define a field that only accepts certain categories, you can use the constrains constructor.

We have the `ProductBase` schema, which is the **base schema for product registration.** This schema is **used to validate the data that is received by the API, and also to define the types of data that are returned by the API.**

We have the `ProductCreate` schema, which is the **schema that is returned by the API.** It is a **class that inherits from the `ProductBase` schema, and has an additional field, which is the `id`.** This field is used to identify the product in the database.

We have the `ProductResponse` schema, which is **the schema that is returned by the API.** It is a class that inherits from the `ProductBase` schema, and **has two more fields, which are `id` and `created_at`. These fields are generated by our database.**

We have the `ProductUpdate` schema, **which is the schema that is received by the API for updating.** It has optional fields, as it is not necessary to send all the fields to update.

## `crud.py` file
The `crud.py` file is responsible for **defining the CRUD functions using the SQLAlchemy ORM.** These functions are **used to communicate with the database.** This is where we **define the functions of listing, creating, updating and removing products.** This is where the data is persisted in the database.

## `router.py` file
The `router.py` file is **responsible for defining API routes using FastAPI.** This is where we define the routes, and also **the functions that will be performed on each route.** All **functions defined here receive one parameter, which is the request parameter, which is the object that contains the request data.**

The **main parameters are path**, which is **the path of the route, methods, which are the HTTP methods that the route accepts, and response_model, which is the schema that is returned by the route.**
```python
@router.post("/products/", response_model=ProductResponse)
```

It is **important to highlight that FastAPI uses the concept of type hints, which are type annotations.** 

This **allows FastAPI to validate the data that is received into the API, and also to define the types of data that are returned by the API.** For example, **when defining the product parameter of type `ProductResponse`, FastAPI already understands that the data received in this parameter must be of type `ProductResponse`.**

We can also **return parameters through our path, in the case of delete**, for example, we need to **pass the `id` of the product we want to delete.** To do this, we use the **path `/products/{product_id}`, and define the `product_id` parameter in the delete_product function.**
```python
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
```

## `main.py` file
The `main.py` file is responsible for **defining the FastAPI application, and also for defining the `Uvicorn web server`.** This is where we **define the web server, and also the web server settings such as the host and port.**


# The Frontend
Our frontend **will be an application that will consume our API, and will be responsible for registering, changing and removing products.** Let's detail each of the folders and files in our frontend.

## `Streamlit`
Streamlit is a **library for building web applications with Python.** It is widely used to build dashboards, and also to **build applications that consume APIs.**

# `Requests`
Requests is a **library for making HTTP requests with Python.** It is **widely used to consume APIs, and also for web scraping.**

# `Pandas`
Pandas is a **library for manipulating data with Python.** It is **widely used to perform data analysis, and also to build dashboards.**