import bs4
import requests
import csv 


base_address = "https://www.kalerkantho.com"
category = "online/education"


all_url = []
for page_index in [i for i in range(18, 21691, 18)]:
    
    complete_url = base_address+'/'+category+'/'+str(page_index)
    print(complete_url)

    all_url.append([complete_url])

    pass

with open('lifestyle_main_page_url.csv', mode='w', newline='') as main_url_list:
    main_url_writer = csv.writer(main_url_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for url in all_url:
        print(url)
        main_url_writer.writerow(url)

main_url_list.close()