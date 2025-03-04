from datetime import date

import requests
import time
from bs4 import BeautifulSoup

def get_house_at(url, cities):
    # read from data base
    print("loading data from seen_house.txt")
    seen_house = set()
    with open("seen_house.txt", "r", encoding="utf-8") as file:
        for line in file:
            seen_house.add(line.strip())  # Removes newline characters
            print(line.strip())

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
            for city in cities:
                if f"VA/{city}" in line:
                    line = line.replace('<loc>', '')
                    line = line.replace('</loc>', '')
                    line = line.strip()
                    if line in seen_house:
                        # print(f"duplicated record {line}")
                        continue
                    if filter(line, session, headers):
                        with open("seen_house.txt", "a", encoding="utf-8") as file:
                            file.write(f"\n{line}")
                        print(line)
        
        
    else:
        print(response.status_code)
        print(response.text)
    

def filter(url, session, headers):
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', attrs={"name": "twitter:text:price"})
    price = meta_tag['content']
    if price not in ['Unknown']:
        price = int(price.replace("$", "").replace(",", ""))
        if price > 1200000 and price < 1600000:
            print(f"${price/1000000}M")
            return True
        else:
            return False
    #print(price) 


if __name__ == "__main__":
    get_house_at("https://www.redfin.com/newest_listings.xml", ['Mc-Lean', 'Vienna', 'Great-Falls', 'Falls-Church'])
