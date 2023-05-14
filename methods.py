import requests
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import yfinance as yf
import json
url = 'https://www.alphavantage.co/query'
apiKey="22C2TB39ZZTB0RDK"

def ListCompanies():
    params = {
        'function': 'LISTING_STATUS',
        'apikey': apiKey
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        df = response.text.split('\n')
        info=[]
        for i in range (1,len(df)-1):
            company=df[i].split(",")
            aux={"symbol":company[0],"name":company[1],"exchange":company[2],"assetType":company[3],"ipoDate":company[4],"delistingDate":company[5],"status":company[6]}
            info.append(aux)
        return (info)
    else:
        return (f'Error en la solicitud: {response.status_code}')

def get_historical_data(symbol: str):
    data = yf.download(symbol, start='2016-01-01')
    df = pd.DataFrame(data)
    json_data = df.to_json(orient='records')
    data=json.loads(json_data)
    return data

def analiys(symbol:str):
    data=get_historical_data(symbol)
    if(len(data)>0):
        return EstadicticaDescriptiva(data,symbol)
    else:
        return {"accepted":False,"symbol":symbol}

def rentabilidad_inversion(money,SYMBOL):
    data = get_historical_data(SYMBOL)
    money = float(money)
    close_prices = []
    for i in range(0,len(data)):
        close_prices.append(data[i]['Close'])
    
    # Regresión lineal
    x = np.arange(len(close_prices))
    y = np.array(close_prices)
    slope, intercept = np.polyfit(x, y, 1)
    
    # Predicción del siguiente valor
    next_value = slope * len(close_prices) + intercept
    rentabilidad = (next_value - close_prices[-1]) / close_prices[-1]
    rentabilidad_total = money+(rentabilidad * money)
    
    return str(rentabilidad_total)
    

def EstadicticaDescriptiva(data,symbol):
    close_prices = []
    for i in range(0,len(data)):
        close_prices.append(data[i]['Close'])
    
      #Calcular media
    n = len(close_prices)
    mean = sum(close_prices) / n
    
    #Calcular mediana
    close_prices.sort()
    if n % 2 == 0:
        median = (close_prices[n//2-1] + close_prices[n//2]) / 2
    else:
        median = close_prices[n//2]
    
    #Calcular moda
    freq = {}
    for price in close_prices:
        if price in freq:
            freq[price] += 1
        else:
            freq[price] = 1
    mode_freq = max(freq.values())
    mode = [price for price, freq in freq.items() if freq == mode_freq][0]
    
    #Calcular desviación estándar
    variance = sum([((x - mean) ** 2) for x in close_prices]) / n
    stdev = variance ** 0.5
    datos = {"symbol":symbol,"media": mean, "mediana": median, "moda": mode, "desviacion": stdev, "varianza": variance,"accepted":True}
    return datos

def estadisticasGrupales(group):
    statics=[]
    ignored=[]
    for i in range(0,len(group)):
        company=analiys(group[i])
        statics.append(company)
    for empresa in statics:
        if empresa["accepted"]:
            cv = empresa["desviacion"] / empresa["media"] * 100
            empresa["cv"] = cv
        else:
            ignored.append(empresa["symbol"])
            statics.remove(empresa)
    empresas_sorted = sorted(statics, key=lambda x: x["cv"])
    empresa_confiable = empresas_sorted[0]["symbol"]
    datos={"rely":empresa_confiable,"analytics":statics}
    return {"accepted":datos,"ignored":ignored}