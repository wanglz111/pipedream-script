import requests
import os


# https://lbs.amap.com/
api_token = ""
# https://github.com/Finb/Bark
bark_key = ""

severe_weather_list = [
    "强风/劲风", "疾风", "大风", "烈风", "风暴", "狂爆风", "飓风", "热带风暴", "霾", "中度霾", "重度霾", "严重霾", "雷阵雨", "雷阵雨并伴有冰雹", "中雨", "大雨", "暴雨", "大暴雨", "特大暴雨", "强阵雨", "强雷阵雨", "极端降雨", "中雨-大雨", "大雨-暴雨", "暴雨-大暴雨", "大暴雨-特大暴雨", "雨雪天气", "雨夹雪", "阵雨夹雪", "冻雨", "雪", "阵雪", "小雪", "中雪", "大雪", "暴雪", "小雪 - 中雪", "中雪-大雪", "大雪-暴雪", "浮尘", "扬沙", "沙尘暴", "强沙尘暴", "龙卷风", "雾", "浓雾", "强浓雾", "轻雾", "大雾", "特强浓雾"
]


def get_weather(city_code='320509'):
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all'.format(
        api_token, city_code)
    r = requests.get(url)
    if r.json()['status'] == '1':
        return r.json()

    send_bark('天气获取失败', '天气获取失败')


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


def handle_weather(weather):
    forecasts = weather['forecasts'][0]
    casts = forecasts['casts']

    return casts


def send_tomorrow_weather(casts):
    try:
        for cast in casts[1:2]:
            date = cast['date']
            dayweather = cast['dayweather']
            daytemp = cast['daytemp']
            nighttemp = cast['nighttemp']
            daywind = cast['daywind']
            daypower = cast['daypower']

            title = '明天天气预报'
            content = '日期：{} \n 气温: {}℃ ~ {}℃ \n 天气:  {} \n 风向:  {} \n 风力:  {} \n'.format(
                date, nighttemp, daytemp, dayweather, daywind, daypower)

        send_bark(title, content)

    except Exception as e:
        send_bark('天气获取失败', '天气获取失败')


def severe_weather_alert(casts):
    try:
        for cast in casts:
            if cast['dayweather'] in severe_weather_list:
                title = '恶劣天气预警'
                content = '恶劣天气预警: 日期: {} \n 白天 \n 恶劣天气种类: {}'.format(
                    cast['date'], cast['dayweather'])
                send_bark(title, content)
                break

            if cast['nightweather'] in severe_weather_list:
                title = '恶劣天气预警'
                content = '恶劣天气预警: 日期: {} \n 夜间 \n 恶劣天气种类: {}'.format(
                    cast['date'], cast['nightweather'])
                send_bark(title, content)
                break

    except Exception as e:
        send_bark('天气获取失败', '天气获取失败')


def temperature_difference_alert(casts):
    interval = 5
    try:
        if abs(int(casts[0]['daytemp']) - int(casts[1]['daytemp'])) > interval or abs(int(casts[0]['nighttemp']) - int(casts[1]['nighttemp'])) > interval:
            title = '温差较大预警'
            content = '日期: {} \n 白天气温: {}℃ \n 夜间气温: {}℃ \n'.format(
                casts[1]['date'], casts[1]['daytemp'], casts[1]['nighttemp'])
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
