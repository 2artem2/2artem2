import requests
import pandas as pd
from bs4 import BeautifulSoup


# Предполагаем, что в CSV файле есть колонки:
# 'url', 'last_http_code',
# 'current_http_code', 'google_analytics_present', 'yandex_metrika_present'

df = pd.read_csv('websitess.csv')


def check_analytics(html):
    # Проверяем наличие кодов Google Analytics и Яндекс.Метрики. 
    # Доработать - не видит наличие кодов Google Analytics и Яндекс.Метрики на некоторых сайтах.
    ga_present = bool(html.find(lambda tag: tag.name == 'script' and 'google-analytics.com' in tag.text))
    ym_present = bool(html.find(lambda tag: tag.name == 'script' and 'mc.yandex.ru' in tag.text))
    return ga_present, ym_present


def get_http_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return "Ошибка доступа"


# Проходим по всем сайтам из списка
for index, row in df.iterrows():
    url = row['url']
    
    # Получаем текущий HTTP статус код
    current_code = get_http_status(url)
    df.at[index, 'last_http_code'] = row['current_http_code']
    df.at[index, 'current_http_code'] = current_code
    
    if current_code == 200 or current_code == 300:  # Это означает, что сайт доступен
        html = BeautifulSoup(requests.get(url).text, 'html.parser')
        ga_present, ym_present = check_analytics(html)
        df.at[index, 'google_analytics_present'] = bool(ga_present)
        df.at[index, 'yandex_metrika_present'] = bool(ym_present)

# Сохраняем обновленную таблицу
df.to_csv('websitess.csv', index=False)
