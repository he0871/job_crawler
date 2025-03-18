from datetime import date

import requests
import time
import csv

from bs4 import BeautifulSoup

def extract_house_info():
    print("loading data from seen_house.txt")
    houses = []
    with open("seen_house.txt", "r", encoding="utf-8") as file:
        for line in file:
            houses.append(line.strip())  # Removes newline characters
            print(line.strip())

    sheet_header = "Address, city, sqft, price, status, tax assessed value, Elementary school, Middle Or Junior School, High School, house type, built year, lot size\n"
    with open("house_details.txt", "w", encoding="utf-8") as file:
        file.write(sheet_header)
    session = requests.Session()
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    records = []
    for house in houses:
        
        response = session.get(house, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        description_tag = soup.find_all('meta', attrs={"name": "description"})
        #print(description_tag[0]['content'])
        descriptions = description_tag[0]['content']
        descriptions = descriptions.split(' ')
        idx = descriptions.index('sq.')
        sqft = descriptions[idx-1].replace('sq. ft', '').replace('.', '').strip()
        address = []
        idx += 3
        while descriptions[idx] not in ['VA']:
            #print(descriptions[idx])
            address.append(descriptions[idx])
            idx += 1
        address[-1] = address[-1].replace(',', '')
        city = address[-1]
        address = ' '.join(address)
        address = address.replace('located at', '')
        print(address)
        row = [address.strip(), city, sqft] 
        meta_tag = soup.find('meta', attrs={"name": "twitter:text:price"})
        price = meta_tag['content']
        if price not in ['Unknown']:
            price = int(price.replace("$", "").replace(",", ""))
        row.append(price)
        house_status = soup.find('span', attrs={"class": "bp-DefinitionFlyout bp-DefinitionFlyout__underline"})
        #print(house_status.contents)
        row.append(house_status.contents[0].strip())
        detail_tags = soup.find_all('span', attrs={"class": "entryItemContent"})
        #interested_fields = ['Year Built', sqft, list_date, sold_date, list_price, sold_price, 'Tax Assessed Value', 'Elementary School', 'Middle Or Junior School', 'High School']
        tax_assessed = -1
        Elementary_school = "unkowns"
        Middle_school = "unkowns"
        High_school = 'unkowns'
        for tag in detail_tags:
            #print(dir(tag))
            #print(tag.contents)
            if 'Tax Assessed Value' in tag.contents[0]:
                tax_assessed = str(tag.contents[1]).replace('<span>$', '').replace('</span>', '').replace(',', '')
        
            if 'Elementary School' in tag.contents[0]:
                Elementary_school = str(tag.contents[1]).replace('<span>', '').replace('</span>', '')

            if 'Middle Or Junior School' in tag.contents[0]:
                Middle_school = str(tag.contents[1]).replace('<span>', '').replace('</span>', '')
            
            if 'High School' in tag.contents[0]:
                High_school = str(tag.contents[1]).replace('<span>', '').replace('</span>', '')
            
        row += [tax_assessed, Elementary_school, Middle_school, High_school]

        key_detail_tags = soup.find_all('div', attrs={'class': 'keyDetails-value'})

        if house_status.contents[0].strip() == 'SOLD':
            key_detail_tags = key_detail_tags[:3]
        else:
            key_detail_tags = key_detail_tags[1:4]

        for key_detail in key_detail_tags[:3]:
            print(key_detail)
            vtext =  key_detail.find('span', attrs={'class': 'valueText'})
            if vtext:
                row.append(vtext.contents[0])
            else:
                row.append(key_detail.contents[0])
           
        
        with open("house_details.txt", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)

        


if __name__ == "__main__":
    extract_house_info()