from django.shortcuts import render
from .models import Timeseriesresults, Timeseriesresultvalues, CvCensorcode, CvQualitycode, Units, Organizations
from django.utils import timezone
import pandas as pd
from django.utils import timezone
import datetime
import hidrocomp
from hidrocomp.series.flow import Flow
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

from functools import reduce
import hydro_api
from hydro_api.ana.hidro.serie_temporal import SerieTemporal
#import matplotlib.pyplot as plt
from django.views.generic import TemplateView

datetime.datetime.now(tz=timezone.utc)

def paginainicial(request):
    context={}
    return render(request, 'index.html',context)

def projeto(request):

    stations = {'39970000': 1}
    result = Timeseriesresults.objects.get(pk=stations['39970000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Date': [], 'Data': []}
    for i in data:
        dic['Date'].append(i[1])
        dic['Data'].append(i[0])
    df = pd.DataFrame(dic)


    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Date': [], 'Data': []}
    for i in data:
        dic['Date'].append(i[1])
        dic['Data'].append(i[0])

    df2 = pd.DataFrame(dic)

    #flow = Flow(station=['39970000', '39980000'], source='ANA')
    #fig, data = flow.gantt(title="Disponibilidade de dados da bacia hidrográfica do Rio Coruripe, AL")
    #pyo.plot(fig, filename="odm2/dados.html")

    fig = px.box(df2, y='Data')
    pyo.plot(fig, filename="odm2/dados.html")



    return render(request, 'odm2/base.html')

def dados(request):



    return render(request, 'odm2/dados.html')

'''def plotly(request):

    stations = {'1036050':1}
    result = Timeseriesresults.objects.get(pk=stations['1036050'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue','valuedatetime')
    dic = {'Date': [], 'Data': []}
    for i in data:
        dic['Date'].append(i[1])
        dic['Data'].append(i[0])
    df = pd.DataFrame(dic)

    return render(request, 'odm2/base.html', context)'''

