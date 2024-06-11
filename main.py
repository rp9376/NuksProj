# app.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from bs4 import BeautifulSoup
from fastapi import Query
import requests



# Database setup
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
    #date = Column(Date, index=True)  # Add date column

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/test/")
def test():
    output = parse_date_string("ponedeljek, 8. april")
    return {"message": "Hello, World!", "date": datetime.now().strftime("%Y-%m-%d"), "test": output}

def parse_menu_file(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    week_info = soup.find('div', class_='section-title').find('h2').text.strip()
    menu_by_day = []

    days = soup.find_all('div', class_='accordion-single')
    for day in days:
        day_name = day.find('button').text.strip()
        items = day.find('ul').find_all('li')
        day_menus = [item.text.strip() for item in items]
        menu_by_day.append([day_name, day_menus])

    return week_info, menu_by_day

def parse_date_string(date_string):
    # Mapping of Slovenian month names to month numbers
    slovenian_months = {
        "januar": 1,
        "februar": 2,
        "marec": 3,
        "april": 4,
        "maj": 5,
        "junij": 6,
        "julij": 7,
        "avgust": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12
    }
    
    # Split the input string by comma and whitespace
    day_name, date_info = date_string.split(", ")
    
    # Extract day and month from date_info
    day, month_name = date_info.split(". ")
    
    # Get current year
    current_year = datetime.now().year
    
    # Get month number from Slovenian month name
    month = slovenian_months[month_name.lower()]
    
    # Format the date string
    #formatted_date = f"{day}_{month}.{current_year}"
    formatted_date = f"{day}_{month}"
    
    return formatted_date


def load_menu_to_db(db: Session, week_info, menu_data):
    for day_name, menu_items in menu_data:
        for item in menu_items:
            existing_menu = db.query(Menu).filter(Menu.week_info == week_info, Menu.day_name == day_name, Menu.menu_item == item).first()
            if existing_menu is None:
                menu_record = Menu(week_info=week_info, day_name=day_name, menu_item=item)
                db.add(menu_record)
            else:
                print("dupe")
    db.commit()

@app.post("/load/")
def load_menus():
    directory_path = "./html_data/"

    db = SessionLocal()
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith('.html'):
                filename = os.path.join(directory_path, filename)
                print("*Parsing file: " + filename)
                
                with open(filename, 'r', encoding='utf-8') as file:
                    file_html_content = file.read()

                week_info, menu_data = parse_menu_file(file_html_content)

                load_menu_to_db(db, week_info, menu_data)

                # Remove this break if you want to process all files
                break

        return JSONResponse(content={"message": "Menus loaded successfully"}, status_code=200)
    

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/menus/")
def get_menus():
    db = SessionLocal()
    try:
        menus = db.query(Menu).all()
        return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.delete("/menus/")
def delete_menus():
    db = SessionLocal()
    try:
        db.query(Menu).delete()
        db.commit()
        print("All menus deleted successfully")
        return JSONResponse(content={"message": "All menus deleted successfully"}, status_code=200)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/menu/{day_string}")
def get_menu(day_string: str):
    db = SessionLocal()
    try:
        out = []
        # Query the database to retrieve menus for the specified day string
        menus = db.query(Menu).all()
        
        print(day_string)  # Print the provided day string
        
        # Filter menus by comparing the parsed day name with the provided day string
        for menu in menus:
            if parse_date_string(menu.day_name) == day_string:
                out.append(menu)
        
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

        ## Js se zelo lepo opravičujem za ta code monstrosity ampak dela

@app.post("/today/")
def load_today_menus():
    url = "https://fe.uni-lj.si/o-fakulteti/restavracija/"
    db = SessionLocal()

    try:
        # Make a GET request to the website
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content

            # Parse the HTML content
            week_info, menu_data = parse_menu_file(html_content)

            # Load menu data into the database
            load_menu_to_db(db, week_info, menu_data)

            return JSONResponse(content={"message": "Today's menus loaded successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch data from {url}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()