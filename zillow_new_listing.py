from datetime import date

import requests
import time
import subprocess

from bs4 import BeautifulSoup

# caffeinate -i python

def send_message(context):
    segments = context.split('/')
    address = segments[-3]
    subprocess.run(['osascript', '-e', f'tell application "Messages" to send "Dear my wife please check the property at {address}: {context}" to buddy "9196380146" of (service 1 whose service type is iMessage)'])

def filter(session, url, headers):
    print("flitering...")
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract Zillow JSON data from script tag
    script_tags = soup.find_all("script")
    price = None
    print(len(script_tags))
    for script in script_tags:
        #print(script.text)
        if "price" in script.text:  # Look for relevant JSON containing price info
            json_text = script.string.strip()
            print(json_text)
            try:
                data = json.loads(json_text)
                price = data.get("price")
                break
            except json.JSONDecodeError:
                continue
    if price:
        print(price)
        price = int(price)
        if price >= 1200000 and price < 1600000:
            return True
    return False


def get_house_at_zipcode(url, zip_codes):
    # read from data base
    print("loading data from seen_house.txt")
    seen_house = set()
    with open("seen_house_zillow.txt", "r", encoding="utf-8") as file:
        for line in file:
            seen_house.add(line.strip())  # Removes newline characters
            #print(line.strip())

    session = requests.Session()
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        today = date.today()
        print("Current Date:", today)
        lines = response.text.split('\n')
        for line in lines:
            #print(line)
            for zip_code in zip_codes:
                if f"-{zip_code}" in line:
                    #print(line)
                    line = line.replace('<loc>', '')
                    line = line.replace('</loc>', '')
                    line = line.strip()
                    if line in seen_house:
                        # print(f"duplicated record {line}")
                        continue

                    #if filter(session, line, headers):
                    #    print(line)
                    
                    with open("seen_house_zillow.txt", "a", encoding="utf-8") as file:
                        file.write(f"\n{line}")
                    print(line)
                    send_message(line)
                    
                    
        
        
    else:
        print(response.status_code)
        print(response.text)

# https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-owner/latest.xml.gz
# https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/latest.xml.gz



if __name__ == "__main__":
    while True:
        get_house_at_zipcode("https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/latest.xml.gz", ['22181', '22180', '22182', '22101', '22102', '22066','22046', '22124'])
        time.sleep(1800)