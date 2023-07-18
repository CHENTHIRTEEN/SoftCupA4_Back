import json
import joblib
import os
from django.http import HttpResponse
import pandas as pd
from rest_framework.decorators import api_view
from .util.toolUtil import datalist, framlist, dfloc


def upload(request) -> HttpResponse:
    """上传文件"""
    # 获取相对路径
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.FILES.get('file', None)
        path = BASE_DIR + '/data'
        file_path = path + f'/{file.name}'
        # 上传文件
        try:
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return HttpResponse(json.dumps({"code": 200, "message": "success"}))
        except FileExistsError:
            return HttpResponse(json.dumps({"code": 100, "message": "发生错误了捏"}))

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
