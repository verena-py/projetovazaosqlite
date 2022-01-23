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
import statsmodels
import openpyxl

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
    dic = {'Data': [], '39970000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39970000'].append(i[0])
    df = pd.DataFrame(dic)


    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39980000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39980000'].append(i[0])
    df2 = pd.DataFrame(dic)

    data_frames = [df, df2]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Data'],
                                                        how='outer'), data_frames)
    df_merged = df_merged.sort_values(by='Data')
    df_merged = df_merged.reset_index(drop=True)
    df_merged['Data'] = df_merged['Data'].apply(lambda a: pd.to_datetime(a).date())

    df_merged.to_excel("/home/verena/Downloads/medicoes_baciacoruripealagoas.xlsx")

    return render(request, 'odm2/base.html')

def mapa(request):
    fig = go.Figure(go.Scattermapbox(
        lat=['-9.4437', '-10.0152'],
        lon=['-36.3014', '-36.1813'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=['ESTAÇÃO'],
    ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.write_html("odm2/mapa.html")

    pyo.plot(fig, filename="odm2/mapa.html")


    return render(request,'odm2/mapa.html')

def dados(request):

    return render(request, 'odm2/dados.html')


def analise(request):
    context = {}

    return render(request, 'odm2/analise.html', context)

def box(request):
    stations = {'39970000': 1}
    result = Timeseriesresults.objects.get(pk=stations['39970000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39970000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39970000'].append(i[0])
    df = pd.DataFrame(dic)


    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39980000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39980000'].append(i[0])
    df2 = pd.DataFrame(dic)

    data_frames = [df, df2]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Data'],
                                                        how='outer'), data_frames)
    df_merged = df_merged.sort_values(by='Data')
    df_merged = df_merged.reset_index(drop=True)

    trace1 = go.Box(y=df_merged['39970000'],
                            name='39970000')
    trace2 = go.Box(y=df_merged['39980000'],
                            name='39980000')
    grafico = [trace1, trace2]

    layout = go.Layout(yaxis={'title': ''},
                           xaxis={'title': ''})
    fig = go.Figure(data=grafico, layout=layout)

    pyo.plot(fig, filename="odm2/box.html")

    return render(request, 'odm2/box.html')

def disp(request):

    stations = {'39970000': 1}
    result = Timeseriesresults.objects.get(pk=stations['39970000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39970000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39970000'].append(i[0])
    df = pd.DataFrame(dic)


    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39980000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39980000'].append(i[0])
    df2 = pd.DataFrame(dic)

    data_frames = [df, df2]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Data'],
                                                        how='outer'), data_frames)
    df_merged = df_merged.sort_values(by='Data')
    df_merged = df_merged.reset_index(drop=True)

    trace1 = go.Scatter(x=df_merged['Data'],
                            y=df_merged['39970000'],
                            mode='markers',
                            name='39970000')
    trace2 = go.Scatter(x=df_merged['Data'],
                            y=df_merged['39980000'],
                            mode='markers',
                            name='39980000')
    grafico = [trace1, trace2]

    layout = go.Layout(title='Gráfico de Dispersão Rio Coruripe',
                           yaxis={'title': 'Dados (mm)'},
                           xaxis={'title': 'Tempo'})
    fig = go.Figure(data=grafico, layout=layout)

    pyo.plot(fig, filename='odm2/disp.html')

    return render(request, 'odm2/disp.html')


def gantt(request):

    flow = Flow(station=['39970000', '39980000'], source='ANA')
    fig, data = flow.gantt(title="Disponibilidade de dados da bacia hidrográfica do Rio Coruripe, AL")
    pyo.plot(fig, filename="odm2/gantt.html")

    return render(request, 'odm2/gantt.html')

def histo(request):
    stations = {'39970000': 1}
    result = Timeseriesresults.objects.get(pk=stations['39970000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39970000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39970000'].append(i[0])
    df = pd.DataFrame(dic)

    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39980000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39980000'].append(i[0])
    df2 = pd.DataFrame(dic)

    data_frames = [df, df2]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Data'],
                                                    how='outer'), data_frames)
    df_merged = df_merged.sort_values(by='Data')
    df_merged = df_merged.reset_index(drop=True)

    layout = go.Layout(title='Histograma Rio Coruripe',
                       yaxis={'title': 'Dados (mm)'},
                       xaxis={'title': 'Tempo'})

    fig = go.Figure(data=[go.Histogram(x=df_merged['39970000'], name='39970000')])
    fig.add_trace(go.Histogram(x=df_merged['39980000'], name='39980000'))

    pyo.plot(fig, filename='odm2/histo.html')

    return render(request, 'odm2/histo.html')

def hidro(request):

    stations = {'39970000': 1}
    result = Timeseriesresults.objects.get(pk=stations['39970000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39970000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39970000'].append(i[0])
    df = pd.DataFrame(dic)


    stations = {'39980000': 2}
    result = Timeseriesresults.objects.get(pk=stations['39980000'])
    data = Timeseriesresultvalues.objects.filter(resultid=result).values_list('datavalue', 'valuedatetime')
    dic = {'Data': [], '39980000': []}
    for i in data:
        dic['Data'].append(i[1])
        dic['39980000'].append(i[0])
    df2 = pd.DataFrame(dic)

    data_frames = [df, df2]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Data'],
                                                        how='outer'), data_frames)
    df_merged = df_merged.sort_values(by='Data')
    df_merged = df_merged.reset_index(drop=True)

    trace1 = go.Scatter(x=df_merged['Data'],
                            y=df_merged['39970000'],
                            mode='lines',
                            name='39970000')
    trace2 = go.Scatter(x=df_merged['Data'],
                            y=df_merged['39980000'],
                            mode='lines',
                            name='39980000')
    grafico = [trace1, trace2]

    layout = go.Layout(title='Hidrograma Rio Coruripe',
                           yaxis={'title': 'Dados (mm)'},
                           xaxis={'title': 'Tempo'})
    fig = go.Figure(data=grafico, layout=layout)

    pyo.plot(fig, filename='odm2/hidro.html')

    return render(request, 'odm2/hidro.html')
