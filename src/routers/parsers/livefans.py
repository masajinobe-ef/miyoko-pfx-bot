import requests
from bs4 import BeautifulSoup

url = 'https://www.livefans.jp/search?option=1&keyword=%E5%87%9B%E3%81%A8%E3%81%97%E3%81%A6%E6%99%82%E9%9B%A8&genre=all&sort=e1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.find_all(
    'div', class_=['whiteBack midBox fes', 'whiteBack midBox']
)


for element in elements:
    h3_tag = element.find('h3').text if element.find('h3') else None
    img_tag = element.find('img')['src'] if element.find('img') else None
    p_tag = element.find('p').text if element.find('p') else None
    a_tag = element.find('a')['href'] if element.find('a') else None

    if a_tag:
        full_link = f'https://www.livefans.jp{a_tag}'
    else:
        full_link = None

    print('h3:', h3_tag)
    print('img:', img_tag)
    print('p:', p_tag)
    print('a:', full_link)
    print('\n')
