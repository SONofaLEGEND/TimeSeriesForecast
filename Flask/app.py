from flask import Flask, render_template, request
from flask import jsonify

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from time import strptime,time,mktime
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.decomposition import PCA
from seaborn import heatmap,pairplot
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from datetime import datetime
import matplotlib.dates as mdates
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
import os
import plotly.graph_objects as go

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST','GET'])
def test():
    file = request.files['file']
    df1 = pd.read_csv(file)
    model = request.form['model']
    manufacturer = request.form['manufacturer']
    price_in_thousands = float(request.form['price_in_thousands'])
    __year_resale_value = float(request.form['__year_resale_value'])
    power_perf_factor = float(request.form['power_perf_factor'])
    df1.columns=[x.lower() for x in df1.columns]
    df3=df1.copy()
    for column in df1.columns:
        if df1[column].isnull().sum():
            df3[column]=df1[column].fillna(df1[column].mean())
    t=mktime(strptime('1/1/2023',"%m/%d/%Y"))
    df4=df3.copy()
    day=24*3600
    df4['days_after_launch']=df3['latest_launch'].apply(lambda x: int((t-mktime(strptime(x,"%m/%d/%Y")))/day))
    df4.drop('latest_launch',axis=1,inplace=True)
    cols=df4.columns.tolist()
    cols.append(cols.pop(cols.index('price_in_thousands')))
    df4=df4[cols]
    def remove_outlier(df):
        num_df_cols=df.select_dtypes(include=[np.number]).columns
        d=pd.DataFrame(columns=df.columns.to_list().append('outlier'))
        for col in num_df_cols:
            mean=df[col].mean()
            std=df[col].std()
            u_limit=mean+3*std
            l_limit=mean-3*std
            out=df[(df[col]<l_limit) | (df[col]>u_limit)].copy()
            out['outlier']=col
            d=pd.concat([out,d])
            df=df[(df[col]>l_limit) & (df[col]<u_limit)]
        return (df,d)
    
    df5,d=remove_outlier(df4)
    df9=df5.copy()
    nam=df9[['model','sales_in_thousands']].sort_values(by='sales_in_thousands').model.values
    encod=OrdinalEncoder(categories=[nam])
    df9.model=encod.fit_transform(df9[['model']])
    df9 = df9.drop('vehicle_type', axis=1)
    name=df9.groupby('manufacturer')['sales_in_thousands'].mean().sort_values().index
    encod2=OrdinalEncoder(categories=[name])
    df9.manufacturer=encod2.fit_transform(df9[['manufacturer']])
    X = df9.drop('sales_in_thousands',axis=1)
    y = df9.sales_in_thousands
    bestfeatures = SelectKBest(score_func=mutual_info_regression,k=10)
    fit = bestfeatures.fit(X,y)
    dbest= pd.DataFrame(fit.scores_,columns=['score'])
    dbest['col_nam']= pd.DataFrame(X.columns)
    dbest.sort_values(by='score',ascending=False,inplace=True)    
    most_related=dbest.col_nam.values[:5]
    df10=df9[most_related].copy()
    df10['sales']=df9.sales_in_thousands
    X_sales=df10.drop('sales',axis=1)
    y_sales=df10.sales
    scale_sales=StandardScaler()
    X_scaled_sales=scale_sales.fit_transform(X_sales)
    X_train , X_test , y_train , y_test = train_test_split(X_scaled_sales,y_sales,test_size=0.2,random_state=1)
    model_rf = RandomForestRegressor(random_state=0)
    model_rf.fit(X_train,y_train)
    res = model_rf.predict(X_test)
    acc = model_rf.score(X_test,y_test)
    res = res.tolist()
    json_res = json.dumps(res)
    ip = [model, manufacturer, price_in_thousands, __year_resale_value, power_perf_factor]
    encoder = OrdinalEncoder()
    ip_encoded = encoder.fit_transform(np.array(ip).reshape(1, -1))
    res = model_rf.predict(ip_encoded)[0]

    return [res]

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    file = request.files['file']
    sales = pd.read_csv(file)
    sales.columns = sales.columns.str.replace(' ','_')
    sales["Order_Date"] = pd.to_datetime(sales["Order_Date"], dayfirst = True).dt.date
    sales["Ship_Date"] = pd.to_datetime(sales["Ship_Date"], dayfirst = True).dt.date
    sales["Month"] = pd.DatetimeIndex(sales["Order_Date"]).month
    sales["Year"] = pd.DatetimeIndex(sales["Order_Date"]).year
    sales["Year_Month"] = sales["Year"].astype(str) + "-" + sales["Month"].astype(str)
    sales["Year_Month"] = pd.to_datetime(sales["Year_Month"]).dt.date
    sales_data = sales[["Year_Month","Sales"]].groupby("Year_Month").sum()
    sales_data = sales_data.sort_values(by="Year_Month")
    model=sm.tsa.statespace.SARIMAX(sales_data['Sales'],order=(1, 1, 0),seasonal_order=(1,1,0,12))
    results=model.fit()
    sales_data['forecast']=results.predict(start=35,end=50,dynamic=True)
    future_dates=[sales_data.index[-1]+ DateOffset(months=x)for x in range(0,36)]
    future_datest_df=pd.DataFrame(index=future_dates[1:],columns=sales_data.columns)
    future_df=pd.concat([sales_data,future_datest_df])

    future_df['forecast'] = results.predict(start = 46, end = 200, dynamic= True)   

    future_df = future_df.reset_index()
    future_df = future_df.rename(columns={"index": "Year_Month"})
    actual_trace = go.Scatter(x=future_df['Year_Month'], y=future_df['Sales'], name='Actual')


    forecast_trace = go.Scatter(x=future_df['Year_Month'], y=future_df['forecast'], name='Forecast')

    fig = go.Figure(data=[actual_trace, forecast_trace])
    fig.update_layout(
        title='Time series forecast',
        xaxis_title='Date',
        yaxis_title='Value'
    )
    future_df.to_csv('forecast_data.csv', index=False)


    graph_path = 'E:\Angular\SalesForecast\Python\plots'
    graph_filename = 'ts_sales.png'
    graph_file = os.path.join(graph_path, graph_filename)
    fig.write_image(graph_file)
    graph_url = 'E:\Angular\SalesForecast\Angular\SalesForecast\src\assets\images\ts_sales.png'
    response = {'status': 'success', 'graph_url': graph_url}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)