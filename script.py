import os
import argparse
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(description='Get bitlink and it"s statistics')
    parser.add_argument('url', help='В качестве аргумента надо указать ссылку')
    args = parser.parse_args()
    url = args.url
    try:
        if is_bitlink(token, url):
            print(f'По вашей ссылке прошли: {count_clicks(token, url)} раз(а)')
        else:
            print(f'Битлинк:  {shorten_link(token, url)}')
    except requests.exceptions.HTTPError:
        print('Такой ссылки не существует!')


def shorten_link(token, url):
    headers = {'Authorization': token}
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {'long_url': url}
    response = requests.post(bitly_url, json=payload, headers=headers)
    response.raise_for_status()
    response = response.json()
    return response['link']


def count_clicks(token, link):
    headers = {'Authorization': token}
    parsed = urlparse(link)
    bitlink = f'{parsed.netloc}{parsed.path}'
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    payload = {'unit': 'day', 'units': '-1'}
    response = requests.get(bitly_url, headers=headers, params=payload)
    response.raise_for_status()
    clicks = response.json()['total_clicks']
    return clicks


def is_bitlink(token, url):
    parsed = urlparse(url)
    bitlink = f'{parsed.netloc}{parsed.path}'
    headers = {'Authorization': token}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok
