# NuksProj
Idk I was forced to try something

FastAPI Application Documentation
Overview
This FastAPI application is designed to parse, load, and serve menus from HTML files and a specific URL. The data is stored in a SQLite database, and various endpoints are provided to interact with the menu data. The application also includes HTML rendering using Jinja2 templates.

Endpoints
Root Endpoints
GET /
Renders the index.html template.

Response:

HTML page with a welcome message.
GET /today/
Renders the today.html template.

Response:

HTML page showing today's menu.
GET /yes/
Renders the everything.html template.

Response:

HTML page showing all menus.
API Endpoints
GET /test/
A test endpoint that returns a welcome message and the current date.

Response:

message: "Hello, World!"
date: Current date in YYYY-MM-DD format.
test: Parsed date string example.
POST /load/
Parses HTML files from the ./html_data/ directory and loads the menu data into the database.

Response:

message: "Menus loaded successfully" if successful.
status_code: 200 if successful, 500 if an error occurs.
GET /menus/
Fetches all menus from the database.

Response:

List of menu objects.
DELETE /menus/
Deletes all menus from the database.

Response:

message: "All menus deleted successfully" if successful.
status_code: 200 if successful, 500 if an error occurs.
GET /menu/{day_string}
Fetches menus for a specific day.

Parameters:

day_string: Day string in the format DD_M.
Response:

List of menu objects for the specified day.
GET /fetch_today/
Fetches today's menu from a specific URL and loads it into the database.

Response:

Today's menu objects if successful.
status_code: 200 if successful, 500 if an error occurs.
Utility Functions
parse_menu_file(html_content)
Parses the provided HTML content to extract menu information.

Parameters:

html_content: HTML content as a string.
Returns:

week_info: Week information string.
menu_by_day: List of menus grouped by day.
parse_date_string(date_string)
Parses a Slovenian date string to a specific format.

Parameters:

date_string: Date string in Slovenian format.
Returns:

formatted_date: Formatted date string in the format DD_M.
load_menu_to_db(db, week_info, menu_data)
Loads menu data into the database.

Parameters:

db: Database session.
week_info: Week information string.
menu_data: List of menus grouped by day.
Returns:

None.
Database Setup
The database is set up using SQLite with SQLAlchemy. The Menu model represents the menu items, including id, week_info, day_name, and menu_item.

python
Copy code
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    week_info = Column(String, index=True)
    day_name = Column(String, index=True)
    menu_item = Column(String)
HTML Templates
The application uses Jinja2 templates to render HTML pages. The templates are located in the static directory.

Running the Application
To run the application, use the following command:

sh
Copy code
uvicorn app:app --reload
This will start the FastAPI server with hot-reloading enabled. The application will be accessible at http://127.0.0.1:8000/.

Dependencies
The application depends on the following Python packages:

fastapi
sqlalchemy
requests
beautifulsoup4
jinja2
uvicorn
Ensure you have these dependencies installed before running the application.