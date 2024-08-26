from flask import Flask, request, jsonify
import yfinance as yf
import random
from datetime import datetime, timedelta
app = Flask(__name__)


@app.route('/kline_max', methods=['GET'])
def kline_max():
    stock_code = request.args.get('stock_code')
    period = request.args.get('period', 'max')
    if stock_code:
        response = get_kline_data_max(stock_code, period)
        return jsonify(response)
    else:
        return jsonify({'error': 'Stock code is required.'}), 400


def get_kline_data_max(stock_code, period='max'):
    if '(' in stock_code:
        stock_code = stock_code.split('(')[0].strip()

    ticker = f"{stock_code}.NS" if not stock_code.endswith('.NS') else stock_code
    stock = yf.Ticker(ticker)
    try:
        hist = stock.history(period=period)
        if not hist.empty:
            return {
                'stock': stock_code,
                'period': period,
                'categories': hist.index.strftime('%Y/%m/%d').tolist(),
                'series': [{
                    'name': 'Kline',
                    'data': hist[['Open', 'Close', 'Low', 'High']].values.tolist()
                }]
            }
        else:
            return {'error': f'No data available for {stock_code} with period {period}.'}
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5288, debug=True)