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

@app.route('/financial-data')
def financial_data():
    balanz_data = {
        'name': 'XYZ',
        'price': 100.25,
        'change': '+1.25%'
    }
    
    investing_pro_data = {
        'name': 'ABC',
        'price': 2500.75,
        'change': '-0.50%'
    }
    
    return render_template('financial_data.html',balanz=balanz_data, investing=investing_pro_data)

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
        'XYZ': 'Acción XYZ',
        'ABC': 'Índice ABC'
    }

    results = {key: value for key, value in data.items() if cedears in value.lower()}

    return results

@app.route('/test')
def test():
    return "Ruta de prueba funciona correctamente"

def test_search():
    cedears_list = ['apple', 'tesla', 'xyz', 'abc', 'nonexistent']
    for cedears in cedears_list:
        print(f"Testing cedears: {cedears}")
        results = search_investments(cedears)
        print(f"Results: {results}")

if __name__ == '__main__':
    test_search()
    app.run(debug=True)
