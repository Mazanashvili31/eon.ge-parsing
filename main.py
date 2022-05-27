import requests
from bs4 import BeautifulSoup
import csv
import time
import random


file = open('books.csv', 'w', newline='\n')
file_object = csv.writer(file)
file_object.writerow(['სახელწოდება', 'ავტორი', 'წელი', 'ქართული გამომცემლობა', 'შეფასება'])
for page_num in range(5):
    url = f'https://eon.ge/books/ჟანრი/ევროპული-ლიტერატურა/page/{str(page_num)}/'
    req = requests.get(url)
    soup_all = BeautifulSoup(req.text, 'html.parser')
    soup = soup_all.find('div', class_='post-list group')

    rows = soup.find_all('div', class_='post-row')

    for row in rows:
        books = row.find_all('article')
        for book in books:
            try:
                book_details = book.find('div', class_='post-thumbnail')
                book_link = book_details.a.attrs['href']
                request = requests.get(book_link)
                another_soup = BeautifulSoup(request.text, 'html.parser')
                title = another_soup.find('h1', class_='post-title').text
                scrap = another_soup.find_all('div', class_='rcno-term-list')
                author_scrap = scrap[0].find('span', class_='rcno-tax-term')
                author = author_scrap.a.text
                publisher_scrap = scrap[2].span.text
                i = 2
                while( publisher_scrap != 'გამომცემლობა: '):
                    i += 1
                    publisher_scrap = scrap[i].span.text
                    if i == 10:
                        break
                publisher_scrap = scrap[i].find('span',class_='rcno-tax-term')
                publisher = publisher_scrap.a.text
                try :
                    year_scrap = another_soup.find('div', class_='rcno_book_pub_date')
                    year = year_scrap.find('span', class_='rcno-meta-value').text
                    year = year.replace('NaN/', '')
                    year = year.replace('NaN', '')
                except:
                    year = 'მითითებული არ არის'
                grade_scrap = another_soup.find('div', class_='rcno_book_gr_review')
                grade = grade_scrap.find('span', class_='rcno-meta-value').text
            except:
                pass
            file_object.writerow([title, author, year, publisher, grade])
            time.sleep(random.randint(15,20))


