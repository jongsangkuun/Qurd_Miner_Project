import requests, json, datetime, pytz
from time import sleep
import psycopg2
from psycopg2 import pool
import urllib3
import configparser
from config import config

url = 'https://urlhaus-api.abuse.ch/v1/urlid/'
http = urllib3.PoolManager()
urlid_key = 3

params = {'urlid':urlid_key}
res_csv = http.request('POST',url,fields=params)
res_csv_json = json.loads(res_csv.data.decode('utf-8'))

for payload in res_csv_json['payloads']:
    print('pay : ',payload['response_md5'])