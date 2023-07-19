import json
import time

import joblib
import os
from django.http import HttpResponse
import pandas as pd
from rest_framework.decorators import api_view
from .util.toolUtil import datalist, framlist, dfloc, size_convert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@api_view(['POST'])
def deletefile(request) -> HttpResponse:
    if request.method == 'POST':
        id = request.POST.get("id")
        path = 'data/' + id + '.csv'
        try:
            os.remove(path)
            return HttpResponse(json.dumps({"code": 200, "message": "success"}))
        except FileNotFoundError:
            return HttpResponse(json.dumps({"code": 100, "message": "error"}))


@api_view(['POST'])
def frammanage(request) -> HttpResponse:
    base = 'data/'
    data = []
    if request.method == 'POST':
        files = datalist()
        for file in files:
            path = base + file
            filemt = time.localtime(os.stat(path).st_mtime)
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", filemt)
            id = file[:2]
            size = size_convert(os.path.getsize(path))
            type = file[-3:]
            temp = {"date": create_time, "id": id, "size": size, "type": type}
            data.append(temp)
    return HttpResponse(json.dumps({"code": 200, "message": "success", "data": data}))


@api_view(['POST'])
def data_process(request) -> HttpResponse:
    """
    数据预处理
    @param request:
    @return:
    """
    if request.method == 'POST':
        file = request.POST.get("file")
        path = 'data/' + file
        try:
            df = pd.read_csv(path)
            if '/' in df.DATATIME[1]:
                datetime = pd.to_datetime(df.DATATIME, format='%d/%m/%Y %H:%M:%S')
                new = datetime.dt.strftime("%Y-%m-%d %H:%M:%S")
                df.DATATIME = new
            df['ROUND(A.WS,1)'].fillna(df['WINDSPEED'], inplace=True)
            df['ROUND(A.POWER,0)'].fillna(df['PREPOWER'], inplace=True)
            df['YD15'].fillna(df['ROUND(A.POWER,0)'], inplace=True)
            df.to_csv(path)
            return HttpResponse(json.dumps({"code": 200, "message": "数据预处理成功"}))
        except IOError:
            return HttpResponse(json.dumps({"code": 100, "message": "数据预处理遇到问题"}))


@api_view(['POST'])
def upload(request) -> HttpResponse:
    """
    上传文件
    @param request:
    @return:
    """
    # 获取相对路径
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        path = BASE_DIR + '/data'
        file_path = path + f'/{file.name}'
        # 上传文件
        try:
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # time.sleep(1.5)
            # datafile = '/data' + f'/{file.name}'
            # df = pd.read_csv(datafile)
            # if '/' in df.DATATIME[1]:
            #     datetime = pd.to_datetime(df.DATATIME, format='%d/%m/%Y %H:%M:%S')
            #     new = datetime.dt.strftime("%Y-%m-%d %H:%M:%S")
            #     df.DATATIME = new
            # df['ROUND(A.WS,1)'].fillna(df['WINDSPEED'], inplace=True)
            # df['ROUND(A.POWER,0)'].fillna(df['PREPOWER'], inplace=True)
            # df['YD15'].fillna(df['ROUND(A.POWER,0)'], inplace=True)
            # df.to_csv('/data' + file.name)
            return HttpResponse(json.dumps({"code": 200, "message": "上传成功"}))
        except IOError:
            return HttpResponse(json.dumps({"code": 100, "message": "发生错误了捏"}))
        # except IOError:
        #     return HttpResponse(json.dumps({"code": 100, "message": "发生错误了捏"}))


@api_view(['POST'])
def getdatarange(request) -> HttpResponse:
    """
    获取风场数据日期起始范围
    @param request:
    @return:
    """
    if request.method == 'POST':
        # TurbID = request.POST.get("TurbID")
        filename = "data/" + request.POST.get("TurbID") + ".csv"
        df = pd.read_csv(filename, usecols=['DATATIME'])
        start = df['DATATIME'].tolist()[0][0:10]
        end = df['DATATIME'].tolist()[-1][0:10]
        return HttpResponse(json.dumps({"code": 200, "message": "success", "start": start, "end": end}))


@api_view(['GET'])
def showframlist(request) -> HttpResponse:
    """
    @param request:
    @return:
    """
    if request.method == 'GET':
        datesets = datalist()
        framsets = framlist(datesets)
        return HttpResponse(json.dumps({"code": 200, "message": "success", "data": framsets}))


@api_view(['POST'])
def predict_dfloc(request) -> HttpResponse:
    '''

    @param request:
    @return:
    '''
    print(request.POST.get("endDatetime"))
    if request.method == 'POST':
        if request.POST.get("TurbID") == '':
            return HttpResponse(json.dumps({"code": 100, "message": "风场号不能为空"}))
        if request.POST.get("startDatetime") == '' or request.POST.get("endDatetime") == '':
            return HttpResponse(json.dumps({"code": 100, "message": "起止时间不能为空"}))
        filename = "data/" + request.POST.get("TurbID") + ".csv"
        df = pd.read_csv(filename, usecols=['DATATIME', 'WINDSPEED', 'WINDDIRECTION', 'TEMPERATURE', 'HUMIDITY',
                                            'PRESSURE', 'ROUND(A.POWER,0)'])

        # start = df[df['DATATIME'].str.startswith(request.startDatetime)].index[0]
        # end = df[df['DATATIME'].str.startswith(request.endDatetime)].index[0]
        # df = df[start:end].drop(['DATATIME'], axis=1)
        try:
            df = dfloc(request.POST.get("startDatetime"), request.POST.get("endDatetime"), df)
        except IndexError:
            return HttpResponse(json.dumps({"code": 100, "message": "选择时间段超出范围"}))
        new_df = df.copy()
        # 导入模型
        model = joblib.load('model/XGB' + request.POST.get("TurbID") + '.pkl')
        res = model.predict(df.drop(['DATATIME', 'ROUND(A.POWER,0)'], axis=1))
        data = {"DATATIME": new_df['DATATIME'].tolist(), "ROUND": new_df['ROUND(A.POWER,0)'].tolist(),
                "YD15": res.tolist()}
        # print(data)
        return HttpResponse(json.dumps({"code": 200, "message": "success", "data": data}))
