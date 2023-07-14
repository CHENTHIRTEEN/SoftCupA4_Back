import json
import joblib

from django.http import HttpResponse
import pandas as pd
from rest_framework.decorators import api_view
from .util.toolUtil import datalist, framlist, dfloc


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
        df = dfloc(request.POST.get("startDatetime"), request.POST.get("endDatetime"), df)
        new_df = df.copy()
        # 导入模型
        model = joblib.load('model/XGB' + request.POST.get("TurbID") + '.pkl')
        res = model.predict(df.drop(['DATATIME', 'ROUND(A.POWER,0)'], axis=1))
        data = {"DATATIME": new_df['DATATIME'].tolist(), "ROUND(A.POWER,0)": new_df['ROUND(A.POWER,0)'].tolist(),
                "YD15": res.tolist()}
        print(data)
        return HttpResponse(json.dumps({"code": 200, "message": "success", "data": data}))
