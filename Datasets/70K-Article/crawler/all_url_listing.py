import bs4
import requests
import csv

all_unit_link = []
main_page_links = []

base_address = "https://www.kalerkantho.com"
category = "online/education"


def get_sub_links(main_page_link):

    global all_unit_link

    page = requests.get(main_page_link)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    newsArticleDivs = soup.find_all("div", {"class": "col-xs-12 col-sm-6 col-md-6 n_row"})


    for newsArticle in newsArticleDivs:
        a_tag = newsArticle.find("a")
        news_link = a_tag['href']
        complete_url = base_address + news_link[1:]

        all_unit_link.append([complete_url])

    pass

def write_csv(list_to_be_inserted):
    with open('lifestyle_unit_page_url.csv', mode='w', newline='') as unit_url_list:
        unit_url_writer = csv.writer(unit_url_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for url in list_to_be_inserted:
            #print(url)
            unit_url_writer.writerow(url)

    unit_url_list.close()

    pass



with open('lifestyle_main_page_url.csv') as main_url_csv:
    readCSV = csv.reader(main_url_csv)

    for row in readCSV:
        main_page_links.append(row[0])

print('+---------------------------------------------------------+')

get_sub_links(main_page_links[5])

for main_link in main_page_links:
    get_sub_links(main_link)
    pass

write_csv(all_unit_link)

print(len(all_unit_link))


