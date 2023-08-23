from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def fetch_details(request):
    if request.method == 'GET':
        details={}
        num_signals=4
        df = pd.read_csv("../../details.csv")
        for i in range(num_signals):
            details[i]={}
            details[i]["signal"]=str(df.loc[i,"signal"])
            details[i]["cnt"]=str(df.loc[i,"cnt"])
            details[i]["flag"]=str(df.loc[i,"flag"])
            details[i]["vehicles"]=str(df.loc[i,"vehicles"])
            details[i]["greentime"]=str(df.loc[i,"greentime"])
            details[i]["image"]=df.loc[i,"image"]
        details=json.dumps(details)
        return JsonResponse(details,safe=False)

def main_output(request):
    return render(request, 'main.html')
