#!/usr/bin/env python3

from bs4 import BeautifulSoup
import os
import json
from collections import defaultdict

def parse_menu_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    week_info = soup.find('div', class_='section-title').find('h2').text.strip()
    menu_by_day = defaultdict(list)

    days = soup.find_all('div', class_='accordion-single')
    for day in days:
        day_name = day.find('button').text.strip()
        items = day.find('ul').find_all('li')
        for item in items:
            menu_by_day[day_name].append(item.text.strip())

    return week_info, menu_by_day

def get_all_menu_data(directory_path):
    all_menu_data = defaultdict(lambda: defaultdict(list))
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            file_path = os.path.join(directory_path, filename)
            week_info, menu_data = parse_menu_file(file_path)
            for day, items in menu_data.items():
                all_menu_data[week_info][day].extend(items)
    return all_menu_data

def format_menu_data(menu_data):
    structured_data = []
    for week, days in menu_data.items():
        week_entry = {'week_info': week, 'days': []}
        for day, items in days.items():
            day_entry = {'day': day, 'items': items}
            week_entry['days'].append(day_entry)
        structured_data.append(week_entry)
    return structured_data

# Example usage
directory_path = "./html_data/"
all_menu_data = get_all_menu_data(directory_path)
formatted_data = format_menu_data(all_menu_data)

# Convert to JSON and print
json_data = json.dumps(formatted_data, ensure_ascii=False, indent=4)
print(json_data)

# Save to a file (optional)
with open('menu_data.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
