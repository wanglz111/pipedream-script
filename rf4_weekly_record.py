import requests
import bs4

url = 'https://rf4game.com/cn/records/weekly'
# response = requests.get(url = url)

# #tabular_body > div.table_content > div > div.records.flex_table > div.rows
# get rows

# response.encoding = 'utf-8'
# html = response.text
# read record.html from ./record.html
# with open('./record.html', 'r', encoding='utf-8') as f:
#     html = f.read()
# soup = bs4.BeautifulSoup(html, 'lxml')
# selector = "#tabular_body > div.table_content > div > div.records.flex_table > div.rows"
# rows = soup.select(selector)
# records = list(rows[0].children)
# # records 只取奇数行
# records = records[1::2]

# record_content = list(records[0].children)[1]

# single_records = list(record_content.children)[1::2]

# # 最高纪录
# highest_record = single_records[0]
# fish = highest_record.select('.fish .text')[0].text.replace('\n', '').replace(' ', '')
# weight = highest_record.select('.weight')[0].text.replace('\n', '').replace(' ', '')
# location = highest_record.select('.location')[0].text.replace('\n', '').replace(' ', '')
# bait = highest_record.select('.bait .bait_icon')[0]['title']
# gamername = highest_record.select('.gamername')[0].text.replace('\n', '').replace(' ', '')
# data = highest_record.select('.data')[0].text.replace('\n', '').replace(' ', '')

# # 剩下记录
# other_records = list(single_records[1].children)[1::2]
# for record in other_records:
#     # fish = record.select('.fish .text')[0].text.replace('\n', '').replace(' ', '')
#     weight = record.select('.weight')[0].text.replace('\n', '').replace(' ', '')
#     location = record.select('.location')[0].text.replace('\n', '').replace(' ', '')
#     bait = record.select('.bait .bait_icon')[0]['title']
#     gamername = record.select('.gamername')[0].text.replace('\n', '').replace(' ', '')
#     data = record.select('.data')[0].text.replace('\n', '').replace(' ', '')
#     print(fish, weight, location, bait, gamername, data)

def get_meta():
    with open('./record.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html

def get_meta_from_website():
    response = requests.get(url = url)
    response.encoding = 'utf-8'
    html = response.text
    return html

def all_records(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    selector = "#tabular_body > div.table_content > div > div.records.flex_table > div.rows"
    rows = soup.select(selector)
    records = list(rows[0].children)
    # records 只取奇数行
    records = records[1::2]
    return records

def get_all_fish(single_records):
    # 最高纪录
    highest_record = single_records[0]
    fish = highest_record.select('.fish .text')[0].text.replace('\n', '').replace(' ', '')
#    其余记录先判读是否存在
    if single_records[1].text == '':
        return

    other_records = list(single_records[1].children)[1::2]
    other_records.insert(0, highest_record)
    for record in other_records:
        weight = record.select('.weight')[0].text.replace('\n', '').replace(' ', '')
        location = record.select('.location')[0].text.replace('\n', '').replace(' ', '')
        bait = record.select('.bait .bait_icon')[0]['title']
        gamername = record.select('.gamername')[0].text.replace('\n', '').replace(' ', '')
        data = record.select('.data')[0].text.replace('\n', '').replace(' ', '')
        print(fish, weight, location, bait, gamername, data)

def get_weekly_fish_record(single_records):
        # 最高纪录
    highest_record = single_records[0]
    fish = highest_record.select('.fish .text')[0].text.replace('\n', '').replace(' ', '')
#    其余记录先判读是否存在
    if single_records[1].text == '':
        return

    other_records = list(single_records[1].children)[1::2]
    record = other_records[-1]
    weight = record.select('.weight')[0].text.replace('\n', '').replace(' ', '')
    number = weight.split('\xa0')[0]
    unit = weight.split('\xa0')[1]
    if unit == '克':
        weight = str(int(number) / 1000) + '千克'
    print(fish + '=' + number)

def main():
    html = get_meta()
    records = all_records(html)
    for record in records:
        record_content = list(record.children)[1]
        single_records = list(record_content.children)[1::2]
        get_weekly_fish_record(single_records)

if __name__ == '__main__':
    main()
