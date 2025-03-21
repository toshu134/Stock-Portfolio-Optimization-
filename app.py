<<<<<<< HEAD
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
=======
from flask import Flask , request , jsonify, render_template, redirect , url_for , flash 
import numpy as np 
from model import MVO , transformation, sharpe_ratio
from board import create_dash_app

app = Flask(__name__)
app.secret_key = 'jp'

before_optimization = {"stock": []}
after_optimization ={}
create_dash_app(app , before_optimization , after_optimization)

@app.route('/')
def first_page():
    return render_template('main.html')


@app.route('/optimize', methods = ['POST', 'GET'])
def optimize():
    
    if request.method == 'POST':
        assets = int(request.form['numStocks'])
        stock =[]
        investment = []
        
        for i in range(assets): 
            stock_name = request.form.get(f'stockName{i}')
            if stock_name:  
                stock.append(stock_name.upper())
            
            invested = request.form.get(f'stockPrice{i}')
            if invested:    
                invested = float(invested)  
                investment.append(invested)
                
        print(stock)
        transformed_data = transformation(stock , investment) 
           
        before_optimization.update({
            "port_variance": transformed_data["port_variance"],
            "cov_matrix": transformed_data["cov_matrix"],
            "cor": transformed_data["cor"],
            "expected_return": transformed_data["expected_returns"],
            "port_risk": transformed_data["port_risk"],
            "portfolio_retur": transformed_data["portfolio_return"],
            "total": transformed_data["total"],
            "weights": transformed_data["weights"],
            "investment": transformed_data["investment"],
            "stock": transformed_data["stock"],
            "daily_returns": transformed_data[ "daily_returns"] 
        })
        
      
        mvo = MVO(transformed_data["expected_returns"], transformed_data["cov_matrix"], transformed_data["total"])     
       
        if mvo["portfolio_return"] < mvo["portfolio_risk"]:
           sharpratio = sharpe_ratio(transformed_data["expected_returns"], transformed_data["cov_matrix"], transformed_data["total"])
           
           after_optimization.update({
              "portfolio_return": sharpratio["portfolio_return"],
              "portfolio_risk": sharpratio["portfolio_risk"],
              "optimal_weight": sharpratio["optimal_weight"],
              "optimal_amount": sharpratio["optimal_amount"]
            }) 
           
        else:
           after_optimization.update({
              "portfolio_return": mvo["portfolio_return"],
              "portfolio_risk": mvo["portfolio_risk"],
              "optimal_weight": mvo["optimal_weight"],
              "optimal_amount": mvo["optimal_amount"]
            })
       
        print(after_optimization["portfolio_return"]) 
            
        return redirect(url_for('dashboard_page'))
    
@app.route('/dashboard')
def dashboard_page():
    return redirect("/dashboard/")
        

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
#return jsonify({ "incorrect": model2["portfolio_return"] })
>>>>>>> ed03e28 (Updated project with latest changes)
