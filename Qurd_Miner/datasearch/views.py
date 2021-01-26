from django.shortcuts import render,redirect,HttpResponse
import requests
import json
from django.contrib import messages
from django.db import connection

# Create your views here.

# def index(request):
#     return render(request,'helloworld.html')

def form(req):
    data = {
        'view':'hidden'
    }
    
    return render(req,'index.html',data)

def Search_Query_indicator(data,data_type):
    cur = connection.cursor()
    cur.execute('select indicator from reputation_data where indicator_type = (select id from reputation_indicator where indicator_name ilike %s) and indicator = %s;',(data_type,data))
    result = cur.fetchone()
    print('Search_Query_indicator = ',result)

    # select * from reputation_data where indicator_type = (select id from reputation_indicator where indicator_name ilike 'MD5') 
    # and indicator = 'c4ca4238a0b923820dcc509a6f75849b';


    if result == None:
        return "결과가 없습니다"
    else:
        return result[0]

def Search_Query_type(a):
    cur = connection.cursor()
    cur.execute('select indicator_name from reputation_indicator where indicator_name ilike \'%s\';'%a)
    result = cur.fetchone()
    # print('Search_Query_type = ',result)
    if result == None:
        return "결과가 없습니다"
    else:
        return result[0]

def View_indicator_type():
    cur = connection.cursor()
    cur.execute('select indicator_name from reputation_indicator;')
    arr = []
    result = cur.fetchall()
    for i in result:
        arr += i
    result = {'Types':arr}
    print(result)
    return arr


def index(req):
    # view = 'hidden'
    data = {
        'view':'hidden'
    }
    if (req.method == None):
        return render(req,'index.html',data)
        
    elif(req.method == 'POST'):
        if(req.POST.get('Search_type') == '' or req.POST.get('Search_data') == ''):
            return render(req,'alert.html')

        else:
            print('POST')
            Search_type = req.POST.get('Search_type')
            print('ID DATA = ',Search_type)
            Search_data = req.POST.get('Search_data')
            print('PW DATA = ',Search_data)

            Search_type_result = Search_Query_type(Search_type)
            Search_indicator_result = Search_Query_indicator(Search_data,Search_type)
            a = View_indicator_type()

            print('View_indicator_type : ',a)
            print(type(a))
            data = {
                'Search_type_result':Search_type_result,
                'Search_indicator_result':Search_indicator_result,
                'view':'visible'
            }
            data.update(a)

            print(data)
            return render(req,'index.html',data)


    else:
        return render(req,'index.html')

    


