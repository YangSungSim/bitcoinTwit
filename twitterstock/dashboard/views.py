from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from db.influxdb_orm import InfluxOrm

influxOrm = InfluxOrm()
# Create your views here.
@api_view(['GET'])
def get_bitcoin(request):
    query = 'select * from bitcoin;'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_korea_bond(request, start_dt, end_dt):
    query = 'from(bucket:"korea_bond")'\
    '|> range(start:0)'
    if (start_dt is not None and end_dt is not None):
        query = 'from(bucket:"korea_bond")'\
            '|> range(start: '+ start_dt+', stop: '+ end_dt+')'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_us_bond(request, start_dt, end_dt):
    query = 'select * from us_bond;'
    if (start_dt is not None and end_dt is not None):
        query = 'select * from us_bond where date > '+ start_dt+' and date < '+ end_dt+';'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_interest(request):
    query = 'from(bucket:"interest")'\
    '|> range(start:0)'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_p2p(request):
    query = 'select * from p2p;'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_realestate(request):
    query = 'select * from realestate;'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_etf(request, start_dt, end_dt):
    query = 'select * from etf;'
    if (start_dt is not None and end_dt is not None):
        query = 'select * from etf where date > '+ start_dt+' and date < '+ end_dt+';'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

@api_view(['GET'])
def get_us_index(request, start_dt, end_dt):
    query = 'select * from us_index;'
    if (start_dt is not None and end_dt is not None):
        query = 'select * from us_index where date > '+ start_dt+' and date < '+ end_dt+';'
    result = influxOrm.select(query=query)
    return Response({'success': 1, 'result': result})

