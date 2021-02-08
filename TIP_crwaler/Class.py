# -*- coding: utf-8 -*-

import requests, json, datetime, pytz
from time import sleep
import psycopg2
from psycopg2 import pool
import urllib3
import configparser
from config import config

class DB: # PSQL과의 통신을 위한 코드
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        threaded_pool = psycopg2.pool.ThreadedConnectionPool(1, 20,**params)
        if(threaded_pool):
            print('DB 연결 성공')
            pool_conn = threaded_pool.getconn()
    except (Exception, psycopg2.DatabaseError) as error:
        print("DB 연결 에러", error)

class ASD:
    print('asbc')

class Service:

    def __init__(self): #초기 설정
        print('------------------------------------------')
        print('Reputation_Indicator 값을 체크합니다')
        indicator = ['URL','MD5','SHA256','FILE_TYPE','SIGNATURE','FILE_NAME']
        services = ['Abuse.ch','Alien_Vault']
        for key in indicator: # 반복문을 통해서 indicator의 값을 DB에서 검색하여 존재하지 않으면 indicator값을 추가함
            Query = ('select indicator_name from reputation_indicator where indicator_name = \'%s\';'%key)
            DB.cur.execute(Query)
            check = DB.cur.fetchall()
            sleep(0.1)
            if(check == []):
                print('Indicator가 없습니다! 새로운 Indicator를 추가합니다!')
                print('New indicator :',key)
                Query = ('insert into reputation_indicator(indicator_name) values(\'%s\');'%key)
                DB.cur.execute(Query)
                sleep(0.1)
                DB.conn.commit()
                
            else:
                print('Find indicator :',key) 
        
        for key in services: # 마찬가지로 services 배열의 값을 순차적으로 조회 후 없으면 추가하여 초기값을 세팅함
            Query = ('select service_name from reputation_service where service_name=\'%s\';'%key)
            DB.cur.execute(Query)
            check = DB.cur.fetchall()
            sleep(0.1)
            if(check == []):
                print('Service가 없습니다! 새로운 Service를 추가합니다!')
                print('New Service :',key)
                Query = ('insert into reputation_service(service_name) values(\'%s\');'%key)
                DB.cur.execute(Query)
                sleep(0.1)
                DB.conn.commit()

            else:
                print('Find Service :',key)

        print('------------------------------------------')

    def search_indicator_type(self,indicator_name): # reputation_indicator에 존재하는 데이터의 타입을 조회하여 해당하는 값의 ID 필드의 값을 리턴
        query = ('select id from reputation_indicator where indicator_name = \'%s\';'%indicator_name)
        DB.cur.execute(query)
        i = DB.cur.fetchone()[0]
        sleep(0.1)
        return i

    def search_service_name(self,service_name): # reputation_service에 존재하는 데이터의 서비스 값을 조회하여 해당하는 값의 ID 필드의 값을 리턴
        query = ('select id from reputation_service where service_name = \'%s\';'%service_name)
        DB.cur.execute(query)
        i = DB.cur.fetchone()[0]
        sleep(0.1)
        return i
                
    def duplicate_data_check(self,data):
        query = ('select indicator from reputation_data where indicator = \'%s\';'%data)
        DB.cur.execute(query)
        i = DB.cur.fetchone()
        sleep(0.1)
        if(i == NULL):
            return 0
        else:
            return 1


    def Search_recent_url_id(self):
        http = urllib3.PoolManager()
        urllib3.disable_warnings()
        recent = 'https://urlhaus-api.abuse.ch/v1/urls/recent/limit/1/'
        sleep(0.1)
        #------------------------------------------
        #recent/limit/1로 접속해서 가장 최근에 등록된 정보의 urlid값을 참고함
        res_recent = http.request('GET',recent)
        res_recent_json = json.loads(res_recent.data.decode('utf-8'))

        for key in res_recent_json['urls']:
            urlid = key['id']
        #print(res_recent_json)
        recent_urlid = int(urlid)
        print('recent_url_id:',recent_urlid)
        return recent_urlid
    
    def Search_last_url_id(selt):
        query = 'select key from reputation_data_abuse order by key desc;'
        DB.cur.execute(query)
        i = DB.cur.fetchone()
        if i == None:
            return 0
        else:
            return i[0]

class Date:
    def Now(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Audit:
    def loging(self,log):
        DB.cur.execute('insert into reputation_audit(id,audit_log,log_date) values(default,%s,%s);',(log,Date().Now()))
        DB.conn.commit()
        sleep(0.1)
    



    
    
