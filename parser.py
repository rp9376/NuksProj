#!/usr/bin/env python3
import requests

def download_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    url = "https://fe.uni-lj.si/o-fakulteti/restavracija/"
    html_content = download_html(url)
    if html_content:
        with open("downloaded_html.html", "wb") as f:
            f.write(html_content)

