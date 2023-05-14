from flask import Flask, jsonify, request
from methods import *
import os
app=Flask(__name__)

@app.route('/companies', methods=['GET'])
def companies():
    return ListCompanies()

@app.route('/company/<string:SYMBOL>', methods=['GET'])
def company(SYMBOL):
    return get_historical_data(SYMBOL)

@app.route('/statics/<string:SYMBOL>', methods=['GET'])
def statics(SYMBOL):
    return analiys(SYMBOL)

@app.route('/investor/<string:SYMBOL>/<string:money>', methods=['GET'])
def invest(SYMBOL,money):
    return rentabilidad_inversion(money,SYMBOL)

@app.route('/statics/analytics', methods=['post'])
def staticsAll():
    group=request.json["companies"]
    return estadisticasGrupales(group)

if __name__=="__main__":
    app.run(debug=True,port=4000)