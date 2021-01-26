# -*- coding: utf-8 -*-

import requests, json, datetime
from time import sleep
import psycopg2
from psycopg2 import pool
import urllib3
import configparser
from config import config

class Connection_db: # PSQL과의 통신을 위한 코드
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


class Service:
    DB = Connection_db

    def __init__(self): #초기 설정
        print('------------------------------------------')
        print('Reputation_Indicator 값을 체크합니다')
        indicator = ['URL','MD5','SHA256','FILE_NAME']
        services = ['Abuse.ch','Alien_Vault']
        for key in indicator: # 반복문을 통해서 indicator의 값을 DB에서 검색하여 존재하지 않으면 indicator값을 추가함
            Query = ('select indicator_name from reputation_indicator where indicator_name = \'%s\';'%key)
            Service.DB.cur.execute(Query)
            check = Service.DB.cur.fetchall()
            sleep(0.1)
            if(check == []):
                print('Indicator가 없습니다! 새로운 Indicator를 추가합니다!')
                print('New indicator :',key)
                Query = ('insert into reputation_indicator(indicator_name) values(\'%s\');'%key)
                Service.DB.cur.execute(Query)
                sleep(0.1)
                Service.DB.conn.commit()
                
            else:
                print('Find indicator :',key) 
        
        for key in services: # 마찬가지로 services 배열의 값을 순차적으로 조회 후 없으면 추가하여 초기값을 세팅함
            Query = ('select service_name from reputation_service where service_name=\'%s\';'%key)
            Service.DB.cur.execute(Query)
            check = Service.DB.cur.fetchall()
            sleep(0.1)
            if(check == []):
                print('Service가 없습니다! 새로운 Service를 추가합니다!')
                print('New Service :',key)
                Query = ('insert into reputation_service(service_name) values(\'%s\');'%key)
                Service.DB.cur.execute(Query)
                sleep(0.1)
                Service.DB.conn.commit()

            else:
                print('Find Service :',key)

        print('------------------------------------------')

    def search_indicator_type(self,indicator_name): # reputation_indicator에 존재하는 데이터의 타입을 조회하여 해당하는 값의 ID 필드의 값을 리턴
        query = ('select id from reputation_indicator where indicator_name = \'%s\';'%indicator_name)
        Service.DB.cur.execute(query)
        i = Service.DB.cur.fetchone()[0]
        sleep(0.1)
        return i

    def search_service_name(self,service_name): # reputation_service에 존재하는 데이터의 서비스 값을 조회하여 해당하는 값의 ID 필드의 값을 리턴
        query = ('select id from reputation_service where service_name = \'%s\';'%service_name)
        Service.DB.cur.execute(query)
        i = Service.DB.cur.fetchone()[0]
        sleep(0.1)
        return i


        
