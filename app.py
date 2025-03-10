from flask import Flask , request , jsonify, render_template, redirect , url_for , flash 
import numpy as np 
from model import MVO , transformation, sharpe_ratio
app = Flask(__name__)
app.secret_key = 'jp'

@app.route('/')
def first_page():
    return render_template('main.html')


@app.route('/submit_portfolio', methods = ['POST', 'GET'])
def portfolio_optimization():
    
    if request.method == 'POST':
        assets = int(request.form['no.'])
        stock =[]
        investment = []
        
        for i in range(1, assets + 1): 
            stock_name = request.form.get("stock"+ str(i))
            if stock_name:  
                stock.append(stock_name.upper())
            
            invested = request.form.get("investment" + str(i))
            if invested:    
                invested = float(invested)  
                investment.append(invested)
        
        transformed_data = transformation(stock , investment)    
        
        model_data = MVO(transformed_data["expected_returns"], transformed_data["cov_matrix"], transformed_data["total"])     
        
        model2 = sharpe_ratio(transformed_data["expected_returns"], transformed_data["cov_matrix"], transformed_data["total"])
        
        return jsonify({
               "incorrect": model2["portfolio_return"] 
            })
        
        

if __name__ == '__main__':
    app.run(debug=True)