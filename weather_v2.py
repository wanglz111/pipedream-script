import requests

# https://dev.qweather.com/
qweather_key = ''
# https://github.com/Finb/Bark
bark_key = ''

severe_weather_list = ['强阵雨', '雷阵雨', '强雷阵雨', '雷阵雨伴有冰雹', '大雨', '极端降雨', '暴雨', '大暴雨', '特大暴雨', '冻雨', '中到大雨', '大到暴雨', '暴雨到大暴雨', '大暴雨到特大暴雨', '强阵雨', '小雪', '中雪', '大雪', '暴雪', '雨夹雪',
                       '雨雪天气', '阵雨夹雪', '阵雪', '小到中雪', '中到大雪', '大到暴雪', '阵雨夹雪', '阵雪', '雪', '薄雾', '雾', '霾', '扬沙', '浮尘', '沙尘暴', '强沙尘暴', '浓雾', '强浓雾', '中度霾', '重度霾', '严重霾', '大雾', '特强浓雾', '热', '冷', '未知']


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


def get_weather():
    url = "https://devapi.qweather.com/v7/weather/7d?key=" + \
        qweather_key + "&location=120.63,31.12"
    r = requests.get(url)
    if r.json()['code'] == '200':
        return r.json()

    send_bark('天气获取失败', '天气获取失败')


def handle_weather(weather):
    forecasts = weather['daily']
    casts = forecasts

    return casts


def send_tomorrow_weather(casts):
    try:
        for cast in casts[1:2]:
            date = cast['fxDate']
            dayweather = cast['textDay']
            daytemp = cast['tempMax']
            nighttemp = cast['tempMin']
            daywind = cast['windDirDay']
            daypower = cast['windScaleDay']

            title = '明天天气预报'
            content = '日期：{} \n 气温: {}℃ ~ {}℃ \n 天气:  {} \n 风向:  {} \n 风力:  {} \n'.format(
                date, nighttemp, daytemp, dayweather, daywind, daypower)

        send_bark(title, content)

    except Exception as e:
        send_bark('天气获取失败', '天气获取失败')


def severe_weather_alert(casts):
    try:
        for cast in casts:
            if cast['textDay'] in severe_weather_list:
                title = '恶劣天气预警'
                content = '日期: {} \n 白天 \n 恶劣天气种类: {}'.format(
                    cast['fxDate'], cast['textDay'])
                send_bark(title, content)
                break

            if cast['textNight'] in severe_weather_list:
                title = '恶劣天气预警'
                content = '日期: {} \n 晚上 \n 恶劣天气种类: {}'.format(
                    cast['fxDate'], cast['textNight'])
                send_bark(title, content)
                break

    except Exception as e:
        send_bark('天气获取失败', '天气获取失败')


# 两天最低气温差超过5, 或两天最高气温差超过5
def temperature_difference_alert(casts):
    interval = 5
    try:
        if abs(int(casts[0]['tempMax']) - int(casts[1]['tempMax'])) > interval or abs(int(casts[0]['tempMin']) - int(casts[1]['tempMin'])) > interval:
            title = '温差较大预警'
            content = '日期: {} \n 最高气温: {}℃ \n 最低气温: {}℃ \n'.format(
                casts[1]['fxDate'], casts[1]['tempMax'], casts[1]['tempMin'])
            send_bark(title, content)

    except Exception as e:
        send_bark('天气获取失败', e)


def main():
    weather = get_weather()
    casts = handle_weather(weather)
    send_tomorrow_weather(casts)
    severe_weather_alert(casts)
    temperature_difference_alert(casts)


if __name__ == '__main__':
    main()
