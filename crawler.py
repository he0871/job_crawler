import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    session = requests.Session()
    basic_url = 'https://www.google.com/about/careers/applications/'
    url = 'https://www.google.com/about/careers/applications/jobs/results/?location=New%20York%2C%20NY%2C%20USA'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}

    response = session.get(url, headers=headers)
    print(response.status_code)
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    #text = soup.get_text()
    #print(text)
    link_list = []
    for link in soup.find_all('a'):
        if 'jobs/results' in link.get('href'):
            link_list.append(basic_url+link.get('href'))
            #print(link.get('href'))
        #print(link.get('href'))

    for app_link in link_list:
        response = session.get(app_link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.get_text())