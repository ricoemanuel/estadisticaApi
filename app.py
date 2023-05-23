from flask import Flask, jsonify, request
from methods import *
import os
app=Flask(__name__)

@app.route('/companies', methods=['GET'])
def companies():
    return ListCompanies()

@app.route('/company/<string:SYMBOL>/<string:fecha>', methods=['GET'])
def company(SYMBOL,fecha):
    return get_historical_data(SYMBOL,fecha)

@app.route('/statics/<string:SYMBOL>/<string:fecha>', methods=['GET'])
def statics(SYMBOL,fecha):
    return analiys(SYMBOL,fecha)

@app.route('/investor/<string:SYMBOL>/<string:fecha>/<string:money>', methods=['GET'])
def invest(SYMBOL,fecha,money):
    return rentabilidad_inversion(money,SYMBOL,fecha)

@app.route('/statics/analytics', methods=['post'])
def staticsAll():
    group=request.json["companies"]
    dates=request.json["dates"]
    return estadisticasGrupales(group,dates)

if __name__=="__main__":
    app.run(debug=True,port=4000)