# -*- coding: utf-8 -*-
from Class import *
from time import sleep

def Abuse():
    service = Service()
    log = Audit()
    recent_url_id = service.Search_recent_url_id()
    last_url_id = service.Search_last_url_id()
    indi = ['response_md5','response_sha256','file_type','signature','filename']
    url = 'https://urlhaus-api.abuse.ch/v1/urlid/'
    http = urllib3.PoolManager()
    log.loging('Abuse.ch 수집 시작')
    db = DB()

    service_idx = service.search_service_name('Abuse.ch')
    print('service_idx :',service_idx)
    if last_url_id == 0:
        last_url_id += 1

    for urlid_key in range(last_url_id,recent_url_id):
        try:
            params = {'urlid':urlid_key}
            res_csv = http.request('POST',url,fields=params)
            sleep(0.1)
            res_csv_json = json.loads(res_csv.data.decode('utf-8')) 
            if res_csv_json['query_status'] == "ok":
                # query = ('insert into reputation_data_abuse(id,service,key,indicator_type,indicator,reg_date,cre_date) values(default,%s,%s,%s,%s,%s,%s);',(service_idx,urlid_key,service.search_indicator_type('URL'),res_csv_json['url'],Date().Now(),res_csv_json['date_added']))
                # print(query)
                db.cur.execute('insert into reputation_data_abuse(id,service,key,indicator_type,indicator,reg_date,cre_date) values(default,%s,%s,%s,%s,%s,%s);',(service_idx,urlid_key,service.search_indicator_type('URL'),res_csv_json['url'],Date().Now(),res_csv_json['date_added']))
                db.conn.commit()
                sleep(0.1)

                print("==========================================")
                print("status :",res_csv_json['query_status'])
                print("url_id :",urlid_key)
                print("url :",res_csv_json['url'])
                
                if res_csv_json['payloads'] == []:
                    print("reg_date :",Date().Now())
                    print("cre_date :",res_csv_json['date_added'])
                    print("response_md5 : NULL")
                    print("response_sha256 : NULL")
                    print("file_type : NULL")
                    print("signature : NULL")
                    print("filename : NULL")
                
                else:
                    for payload in res_csv_json['payloads']:
                        print("reg_date :",Date().Now())
                        print("cre_date :",res_csv_json['date_added'])
                        print("response_md5 :",payload['response_md5'])
                        print("response_sha256 :",payload['response_sha256'])
                        print("file_type :",payload['file_type'])
                        print("signature :",payload['signature'])
                        print("filename :",payload['filename'])
                        print("\n")
                        
                        # if payload['file_type'] == "unknown":
                        #     continue

                        for j in indi:
                            if j == 'response_md5':
                                a = 'MD5'
                             
                            elif j == 'response_sha256':
                                a = 'SHA256'
                              
                            elif j == 'file_type':
                                a = 'FILE_TYPE'
                            
                            elif j == 'signature':
                                a = 'SIGNATURE'
                        
                            elif j == 'filename':
                                a = 'FILE_NAME'
                                

                            if payload[j] == '' or payload[j] == None or payload[j] == 'unknown' or payload[j] == 'NONE':
                                pass
                            
                            else:
                                sleep(0.1)
                            
                                db.cur.execute('insert into reputation_data_abuse(service,key,indicator_type,indicator,reg_date,cre_date) values(%s,%s,%s,%s,%s,%s);',(service_idx,urlid_key,service.search_indicator_type(a),payload[j],Date().Now(),res_csv_json['date_added']))
                                sleep(0.1)
                                db.conn.commit()
                        
                            
            else:
                print(urlid_key,'=','no_result')

        except Exception as error:
            print(error)
            
        sleep(0.1)
    

    log.loging('Abuse.ch 수집 종료')
                        


Abuse()

