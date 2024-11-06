from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from db.influxdb_orm import InfluxOrm
from db.postgres_orm import PostgresOrm
import json
import pandas as pd

influxOrm = InfluxOrm()
postgresOrm = PostgresOrm()
# Create your views here.
@api_view(['GET'])
def get_bitcoin(request):
    query = 'select * from bitcoin;'
    query = '''
    from(bucket: "bitcoin")
    |> range(start: -3600h)
    '''

    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_korea_bond(request):
    query = 'select * from korea_bond'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[item_name, str(close), change, one_month, six_month, one_year] for index, item_name, close, change, one_month, six_month, one_year  in result], columns=['item_name','close','change','one_month','six_month','one_year'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_us_bond(request):
    query = 'select * from us_bond'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[item_name, str(close), change, one_month, six_month, one_year] for index, item_name, close, change, one_month, six_month, one_year  in result], columns=['item_name','close','change','one_month','six_month','one_year'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_interest(request):
    query = 'select * from interest'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[submitpn, banknm, goodnm, wayre, materityinterest, priority, limit_rate, retarget, atmost, interestnm, typesave, period, interestrate, maxinterest] for index, submitpn, banknm, goodnm, wayre, materityinterest, priority, limit_rate, retarget, atmost, interestnm, typesave, period, interestrate, maxinterest  in result], columns=['submitpn', 'banknm', 'goodnm', 'wayre', 'materityinterest', 'priority', 'limit_rate', 'retarget', 'atmost', 'interestnm', 'typesave', 'period', 'interestrate', 'maxinterest'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_p2p(request):
    query = 'select * from p2p'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[information] for index, information  in result], columns=['information'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_realestate(request):
    query = 'select * from realestate'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[case_id, house_type, address, spec, senior_tenant, appraisal, lowest_price, decline_time] for index, case_id, house_type, address, spec, senior_tenant, appraisal, lowest_price, decline_time  in result], columns=['case_id', 'house_type', 'address', 'spec', 'senior_tenant', 'appraisal', 'lowest_price', 'decline_time'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_etf(request):
    query = 'select * from etf'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[item, close, date] for index, item, close, date  in result], columns=['item', 'close', 'date'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})

@api_view(['GET'])
def get_us_index(request):
    query = 'select * from us_index'
    result = postgresOrm.select(query=query)
    data = pd.DataFrame([[item, close, date] for index, item, close, date  in result], columns=['item', 'close', 'date'])

    json_data = data.to_json(orient='records')
    return Response({'success': 1, 'result': json.loads(json_data)})
