import os
import requests
import boto3
import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from botocore.exceptions import NoCredentialsError
from typing import Optional


# Функция для определения к какой группе относится каждый элемент фида

def load_config(key: Optional[str] = None):
    # Получение абсолютного пути к директории, где находится main.py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Объединение этого пути с именем файла, который вы хотите открыть
    file_path = os.path.join(current_directory, "config.json")

    with open(file_path, "r") as file:
        config = json.load(file)

    if key:
        if key not in config:
            raise KeyError(f"The key '{key}' was not found in the config file.")
        return config[key]  # Возвращаем значение заданного ключа
    else:
        return config  # Возвращаем весь конфигурационный словарь


def determine_group(title):
    if 'Zavtracast' in title or 'Завтракаст' in title:
        return 'Завтракаст'
    elif 'DTKD' in title or 'ДТКД' in title:
        return 'ДТКД'
    elif 'Сказки Дядюшки Зомбака' in title or 'СДЗ' in title:
        return 'СДЗ'
    elif 'Кабинет Лора' in title:
        return 'Кабинет Лора'
    elif 'Special' in title or 'специальный выпуск' in title.lower():
        return 'Special'
    else:
        return 'Другое'


# Функция создания элементов RSS фида для каждого подкаста
def create_rss_feed(group_name, items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    title = ET.SubElement(channel, "title")
    title.text = f"{group_name} Podcast Feed"
    link = ET.SubElement(channel, "link")
    link.text = load_config("web_site")
    description = ET.SubElement(channel, "description")
    description.text = f"This is an RSS feed for the {group_name} series of podcasts."

    for item in items:
        item_element = ET.SubElement(channel, "item")
        item_title = ET.SubElement(item_element, "title")
        item_title.text = item.find('title').text
        item_link = ET.SubElement(item_element, "link")
        item_link.text = item.find('link').text if item.find('link') is not None else "https://www.example.com"
        item_description = ET.SubElement(item_element, "description")
        item_description.text = item.find('description').text if item.find(
            'description') is not None else "No description available"
        item_pubDate = ET.SubElement(item_element, "pubDate")
        item_pubDate.text = item.find('pubDate').text if item.find(
            'pubDate') is not None else "No publication date available"

    feed_str = ET.tostring(rss, encoding='utf-8', method='xml')
    dom = parseString(feed_str)
    pretty_feed_str = dom.toprettyxml(indent="  ")

    return pretty_feed_str


# Функция загрузки XML-фида в Yandex Object Storage
def upload_to_s3(file_name, xml_content, bucket_name):
    s3 = boto3.client('s3', endpoint_url=load_config('ENDPOINT_URL'),
                      aws_access_key_id=load_config('ACCESS_KEY'),
                      aws_secret_access_key=load_config('SECRET_KEY')
                      )
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=xml_content)
        print(f"File {file_name} uploaded to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")


# Функция для анализа исходного фида и его разбивки на группы
def parse_and_group_feed(feed_content):
    root = ET.fromstring(feed_content)
    items = root.findall('./channel/item')

    podcast_groups = {
        'Завтракаст': [],
        'ДТКД': [],
        'СДЗ': [],
        'Кабинет Лора': [],
        'Special': [],
        'Другое': []
    }

    for item in items:
        title = item.find('title').text
        group = determine_group(title)
        podcast_groups[group].append(item)

    return podcast_groups


# Имя вашего бакета в Yandex Object Storage
bucket_name = load_config('BUCKET_NAME')

feed_url = load_config("zavtracast_patreon_feed")
response = requests.get(feed_url)
response.raise_for_status()  # Это выбросит исключение, если запрос не успешен
feed_content = response.text

# Разбор фида и группировка подкастов
podcast_groups = parse_and_group_feed(feed_content)

# Создание и загрузка фидов для каждой группы
for group_name, items in podcast_groups.items():
    if items:  # только если есть подкасты в группе
        feed_xml = create_rss_feed(group_name, items)
        file_name = f'{group_name}_feed.xml'
        upload_to_s3(file_name, feed_xml, bucket_name)
