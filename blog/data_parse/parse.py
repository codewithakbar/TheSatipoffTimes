import re
import csv
import json
import random
import requests
from time import sleep
from turtle import title
from bs4 import BeautifulSoup

# url = "https://daryo.uz/category/mahalliy/"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"

}

# req = requests.get(url, headers=headers)

# src = req.text
# # print(src)

# # with open("blog/data_parse/index_daryo.html", "w", encoding="utf-8-sig") as file:
# #     file.write(src)


# with open("blog/data_parse/index_daryo.html", encoding="utf8") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="itemTitle")

# mahalliy_catigories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://daryo.uz" + item.a["href"]

#     # print(item_href)
#     # print(item_text)

#     mahalliy_catigories_dict[item.text] = item_href

# with open("blog/data_parse/mahalliy_cat_dict.json", "w", encoding="utf8") as file:
#     json.dump(mahalliy_catigories_dict, file, indent=4, ensure_ascii=False) 


with open("blog/data_parse/mahalliy_cat_dict.json", encoding="utf8") as file:
    mahalliy_catigories = json.load(file)

interation_count = int(len(mahalliy_catigories)) - 1
count = 0
print(f"Vsevo iteratsie: {interation_count}")
for category_name, category_href in mahalliy_catigories.items():


    rep = [",", " ", "-", "'", "‘", "“", "?", "!"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"blog/data_parse/data/{count}_{category_name}.html", "w", encoding="utf8") as file:
        file.write(src)

    with open(f"blog/data_parse/data/{count}_{category_name}.html", encoding="utf8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # proverka stranitsi na nalichie tablitsi s productam
    # alert_block = soup.find(class_="uk-alert-danger")
    # if alert_block is not None:
    #     continue


     # sobiraem dannie producda
    post_contents = []
    post_title = soup.find_all(class_="articleCont")

    for item in post_title:
        item_text = item.find(class_="articleContHead").find("h1").text
        item_categ = item.find(class_="articleContHead").find(class_="itemCat").find("a").text
        item_post_cont = item.find(class_="articleContHead").find(class_="postContent")

        post_contents.append(
            {
                "Title": item_text,
                "Category": item_categ,
                "Content": item_post_cont
            }
        )

        with open(f"blog/data_parse/data/{count}_{category_name}.csv", "a", encoding="utf8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        item_text,
                        item_categ,
                        item_post_cont
                    )
                )

    with open(f"blog/data_parse/data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(post_contents, file, indent=4, ensure_ascii=False)
    