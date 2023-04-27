import requests
import bs4

bark_key = "HaNJZPZJyMpSoNp2QLnrM8"

def get_tag_notice():
    url = 'https://note.boccc.co/'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    contents = soup.find('div', id='posts-wrapper')
    contents = contents.find_all('div', class_='post')
    return contents


def handle_tag_notice(contents):
    tag_notices = []
    for content in contents:
        tag_notice = {}
        notice_type = content.find('h1', class_='entry-title').text.replace('#', '')
        # <p><span class="day">03</span>3月 / 2023</p>
        raw_notice_date = content.find('div', class_='date').find('p')
        day = raw_notice_date.find('span', class_='day').text
        month = raw_notice_date.text.split('/')[0].strip().replace(day, '')
        year = raw_notice_date.text.split('/')[1].strip()
        notice_date = f'{year}-{month}-{day}'
        notice_content = content.find('div', class_='entry-content').text
        tag_notice.update(
            {'type': notice_type, 'date': notice_date, 'content': notice_content})
        tag_notices.append(tag_notice)
    return tag_notices


def post_to_jsonbase(tag_notices):
    headers = {
        # Already added when you pass json=
        # 'content-type': 'application/json',
    }

    response = requests.put(
        'https://jsonbase.com/lucas/tags', headers=headers, json=tag_notices)

    return response

def get_from_jsonbase():
    response = requests.get('https://jsonbase.com/lucas/tags')
    if response.status_code == 200:
        return response.json()

def send_bark(title, content):
    url = 'https://api.day.app/{}'.format(bark_key)

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    json_data = {
        'body': content,
        'title': title,
    }

    response = requests.post(url, headers=headers, json=json_data)

def compare_notices(tag_notices, old_notices):
    for notice in tag_notices:
        if notice not in old_notices:
            send_bark(notice['type'], notice['content'] + '\n' + notice['date'])

def main():
    contents = get_tag_notice()
    tag_notices = handle_tag_notice(contents)
    old_notices = get_from_jsonbase()
    compare_notices(tag_notices, old_notices)
    response = post_to_jsonbase(tag_notices)


if __name__ == '__main__':
    main()
