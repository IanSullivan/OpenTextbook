# importing modules
import urllib.request
from bs4 import BeautifulSoup as soup
import textwrap
import git

# providing url
main_url = 'https://biz.libretexts.org/Bookshelves/Marketing/Book%3A_Introducing_Marketing_(Burnett)/02%3A_Understanding_and_approaching_the_market'
main_html = urllib.request.urlopen(main_url)
main_htmlParse = soup(main_html, 'html.parser')
main_title_box = main_htmlParse.findAll('a', attrs={'class': 'internal'})
for a in main_title_box:
    url = a.attrs['href']

    html = urllib.request.urlopen(url)
    htmlParse = soup(html, 'html.parser')
    title = htmlParse.find('title').string
    title = title.replace(" ", "_")
    title = title.replace("?", "")
    title = title.replace(":", " ")
    paragrahs = htmlParse.find_all("p")
    with open('{}.txt'.format(title), 'w') as f:
        for i, para in enumerate(paragrahs):
            if i < 5:
                continue
            if i > len(paragrahs) - 3:
                break
            f.write(textwrap.fill(para.get_text(), 157))
            f.write('\n')