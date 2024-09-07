import os
from flask import Flask, render_template,request
app= Flask (__name__,template_folder=os.path.join(os.path.dirname(__file__),'templates'))

@app.route ('/')
def home():
    return render_template ('home.html')

@app.route ('/about')
def about():
    return render_template('about_investing.html')

@app.route('/index')
def index():
    return render_template('index_balanz.html')

@app.route('/financial-data')
def financial_data():
    balanz_data = {
        'name': 'Acción XYZ',
        'price': 100.25,
        'change': '+1.25%'
    }
    
    investing_pro_data = {
        'name': 'Índice ABC',
        'price': 2500.75,
        'change': '-0.50%'
    }
    return render_template('financial_data.html',balanz=balanz_data, investing=investing_pro_data)

if __name__ == '__main__':
    app.run(debug=True)
