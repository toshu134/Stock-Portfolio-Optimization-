# Stock Portfolio Optimization

## 📌 Project Overview
This project is a **Stock Portfolio Optimization** tool that helps users optimize their investment portfolios. The backend is built using **Flask**, and it processes financial data stored in `stock_data.csv`, which has been extracted from Yahoo Finance using Python.

## 📂 Project Structure
```
├── templates/              # HTML templates for the frontend
├── app.py                  # Main Flask application
├── optimization.py         # Contains the portfolio optimization logic
├── stock_data.csv               # Pre-stored stock data extracted from Yahoo Finance
├── requirements.txt        # Required dependencies
├── README.md               # Project documentation
```

## ⚙️ Features
- **Portfolio Optimization:** Helps users allocate stocks efficiently on the basis of the historical data extracted from yahoo finance 
- **Optimization model:** Uses two models to increase optimization accuracy and secure against single model failure.
- **Flask API:** Processes optimization requests and returns optimized values.
- **Frontend Dashboard:** Displays portfolio analytics and optimization results with interactive visualizations.

## User Input 
![image](https://github.com/user-attachments/assets/9a917606-1676-4a14-882c-72609c73f053)

## 📊 Dashboard Information
The **Dashboard** provides an analytical view of: 
- **Stock analysis tab:** Provides a comprehensive overview of individual stocks, including historical performance and key metrics.
- **Risk-Return Analysis:**  Offers in-depth insights into the portfolio's composition, displaying risk-return analysis and asset distribution through interactive graphs.
- **Historical Performance:** Visualizes the improved portfolio after optimization, highlighting allocation adjustments for better performance..
![image](https://github.com/user-attachments/assets/94d7cc34-52ee-4850-8ede-985c1bfb0e26)
![Screenshot 2025-03-22 030522](https://github.com/user-attachments/assets/1c5a29b9-da2c-48f6-8358-ed2d85020f3f)
![Screenshot 2025-03-22 030532](https://github.com/user-attachments/assets/6787bf1d-9c6d-4861-b206-7793b32bbb7d)


## 🔧 Installation
1. Clone the repository:
   ```sh
   git clone <your-repo-link>
   cd <your-repo-folder>
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```sh
   python app.py
   ```

## 🛠 Technologies Used
- **Python** (Flask, Pandas, NumPy)
- **Yahoo Finance API** (for extracting stock data)
- **HTML/CSS & JavaScript** (for the frontend)
- **Plotly** (for data visualization on the dashboard)

## 📬 Contributions & Issues
Feel free to open an **issue** or **pull request** if you have suggestions or improvements!

---

🚀 **Happy Investing!**

