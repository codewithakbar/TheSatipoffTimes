
from itertools import count
import json
import requests
from fake_useragent import UserAgent

ua = UserAgent()
# print(ua.random)


def collect_data(cat_type):
    """
    cat_type: 2 pichoq, 4 snioer, 13 perchatki
    """
    # response = requests.get(
    #     url = 'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset=0&type=2&withStack=true',
    #     headers={'user-agent': f"{ua.random}"}
    # )

    # with open('result.json', 'w', encoding="utf8") as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)

    offset = 0
    batch_size = 60
    result = []
    count = 0

    while True:
        for item in range(offset, offset + batch_size, 60):
            # url = item
            # print(url)
            
            url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=2000&offset={item}&type={cat_type}&withStack=true'
            response = requests.get(
                url=url,
                headers={'user-agent': f"{ua.random}"}
            )

            offset += batch_size

            data = response.json()
            items = data.get('items')

            for i in items:
                if i.get('overprice') is not None and i.get('overprice') < - 10:
                    item_full_name = i.get('fullName')
                    item_3d = i.get("3d")
                    item_price = i.get("price")
                    item_over_price = i.get("overprice")

                    result.append(
                        {
                            'full_name': item_full_name,
                            '3d': item_3d,
                            'overprice': item_over_price,
                            'item_price': item_price
                        }
                        

                    )

        count += 1
        print(f"Page #{count}")
        print(url)


        if len(items) < 60:
            break
    
    with open("blog/data_parse/result.json", "w", encoding='utf8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(len(result))

def main():
    collect_data(4)

if __name__ == '__main__':
    main()