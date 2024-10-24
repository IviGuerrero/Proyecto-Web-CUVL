import os
from flask import Flask, render_template,request
app= Flask (__name__,template_folder=os.path.join(os.path.dirname(__file__),'templates'))

@app.route ('/')
def home():
    print (f"Template folder: {app.template_folder}")
    return render_template ('home.html')

@app.route ('/investing')
def investing():
    return render_template('investing.html')

@app.route('/balanz')
def balanz():
    return render_template('balanz.html')

@app.route('/iol')
def iol():
    return render_template('iol.html')

@app.route('/analisis')
def analisis():
    return render_template('analisis.html')

@app.route('/search', methods=['GET'])
def search():
    cedears = request.args.get('cedears', '')
    print(f"Search cedears: {cedears}")
    results = search_investments(cedears)
    print(f"Search results: {results}")
    return render_template('search_results.html', cedears=cedears, results=results)

def search_investments(cedears):
    if cedears:
        cedears = cedears.lower()
    else:
        return {}

    data = {
        'AAPL': 'Apple Inc.',
        'TSLA': 'Tesla Motors',
    }
    results = {key: value for key, value in data.items() if cedears in value.lower()}
    return results

@app.route('/test')
def test():
    return "Ruta de prueba funciona correctamente"

def test_search():
    cedears_list = ['apple', 'tesla', 'nonexistent']
    for cedears in cedears_list:
        print(f"Testing cedears: {cedears}")
        results = search_investments(cedears)
        print(f"Results: {results}")

@app.route('/logo')
def logo():
    return render_template ('logo.html')

@app.route('/trading', methods=['GET'])
def trading():  
    return render_template('trading.html')

@app.route('/grafico')
def grafico():
    return render_template('grafico.html')

if __name__ == '__main__':
    app.run(debug=True)
