import numpy as np 
from scipy.optimize import minimize
import pandas as pd
import seaborn as sns

def transformation( stocks , investment ):
    file = "C://Users//Arnav Singh//OneDrive//Desktop//Portfolio Optimizer//stock_data.csv"
    
    df = pd.read_csv(file)
    df = df.drop('Date', axis=1)
    pct_return = df.pct_change().iloc[1:]
    
    #dataset data
    cov = pct_return.cov()*252 #covariance of dataset annually
    expected_return = pct_return.mean()*252 #mean per column annualy
    total = sum(investment)
    weights = np.array([i/total for i in investment])
    
    #extracting the dataset data according to user portfolio 
    new_df = pct_return[stocks]
    cor = new_df.corr()
    cov_selected = cov.loc[stocks, stocks]    
    expected_return_selected  = expected_return[stocks]

    #calculated the variance of portfolio  formula w ⋅(Σ⋅w)
    port_variance = np.round(np.dot(weights.T, np.dot(cov_selected, weights)),4)
  
    port_volatality = np.sqrt(port_variance) #standard deviation(volatality of portfolio )
    port_volatality = round(port_volatality*100,2)
       
    portfolio_annual_return = np.sum(expected_return_selected*weights)
    portfolio_annual_return= round(portfolio_annual_return*100,2)
    
    return {
    "cor": cor, 
    "cov_matrix": cov_selected,
    "port_variance": port_variance,
    "expected_returns": expected_return_selected,
    "port_risk": port_volatality,
    "portfolio_return": portfolio_annual_return,
    "total": total,
    "stock": stocks,
    "investment": investment,
    "weights": weights,  
    "daily_returns": new_df  
}

  
  
def MVO(expected_return_selected, cov_selected, total):
    mu = expected_return_selected  
    sigma = cov_selected           
    num_stocks = len(expected_return_selected) 

    
    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(sigma, weights))

   
    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
    )

    
    bounds = [(0, 0.5) for _ in range(num_stocks)]

    
    initial_guess = np.array([1 / num_stocks] * num_stocks)

    
    result = minimize(portfolio_variance, initial_guess, bounds=bounds, constraints=constraints)

    # Check if optimization was successful
    if result.success:
        optimal_weights = result.x  
        rounded_weights = np.round(optimal_weights, 2)

        portfolio_return = round(np.sum(rounded_weights*mu)*100,2)
        
        # Calculate portfolio volatility (standard deviation)
        portfolio_variance_value = portfolio_variance(optimal_weights)
        portfolio_volatility = round(np.sqrt(portfolio_variance_value)*100,2)
    
    o_amount = np.round(np.dot(rounded_weights,total),2)
    
    return {
            "portfolio_return": portfolio_return,
            "portfolio_risk": portfolio_volatility,
            "optimal_amount": o_amount.tolist(),
            "optimal_weight" : rounded_weights.tolist()
        }
    


def sharpe_ratio(expected_return2, cov2 , total ):
    risk_free_rate = 0
    target_returns = np.linspace(min(expected_return2.values), max(expected_return2.values), 100)

    efficient_volatilities = []
    efficient_returns = []
    efficient_weights = []

    for target in target_returns:
        
        constraints = (
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},  # Sum of weights = 1
        )

        bounds = [(0, 0.5) for _ in range(len(expected_return2.values))]
        # Initial guess for weights
        initial_guess = np.array([1 / len(expected_return2.values)] * len(expected_return2.values))

        result = minimize(lambda w: np.dot(w.T, np.dot(cov2.values, w)),initial_guess, method="SLSQP", bounds=bounds, constraints=constraints)

        # Store results if optimization is successful
        if result.success:
            efficient_volatilities.append(np.sqrt(result.fun))  # Portfolio risk (volatility)
            efficient_returns.append(target)  # Portfolio return
            efficient_weights.append(result.x)

    # Calculate Sharpe Ratios
    sharpe_ratios = [(r - risk_free_rate) / v for r, v in zip(efficient_returns, efficient_volatilities)]

    # Find the portfolio with the maximum Sharpe Ratio
    max_sharpe_idx = np.argmax(sharpe_ratios)
    max_sharpe_return = round(efficient_returns[max_sharpe_idx]*100, 2)
    max_sharpe_volatility = round(efficient_volatilities[max_sharpe_idx]*100,2)
    max_sharpe_weights = efficient_weights[max_sharpe_idx]
    max_sharpe_weights = np.round(max_sharpe_weights,2)
    o_amount = np.round(np.dot(max_sharpe_weights, total),2)
    
    return{
        "portfolio_return":max_sharpe_return,
        "portfolio_risk": max_sharpe_volatility,
        "optimal_amount":o_amount.tolist(),
        "optimal_weight": max_sharpe_weights.tolist()
    }

