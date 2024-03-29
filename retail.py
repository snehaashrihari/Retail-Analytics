
####Importing all the packages as necessary
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy.stats.mstats import winsorize
# %matplotlib inline

import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
print(__version__) # requires version >= 1.9.0
import plotly.graph_objects as go
import cufflinks as cf
cf.go_offline()

def enable_plotly_in_cell():
  import IPython
  from plotly.offline import init_notebook_mode
  display(IPython.core.display.HTML('''<script src="/static/components/requirejs/require.js"></script>'''))
  init_notebook_mode(connected=False)
    
from google.colab import files
upload =files.upload()
upload =files.upload()
upload =files.upload()
customer=pd.read_csv('Customer - Copy.csv')
prod_cat=pd.read_csv('prod_cat_info.csv')
transaction=pd.read_csv('Transactions3.csv')
transaction=transaction.drop_duplicates()
transaction=transaction[transaction['Qty']>0]  ###Removing the negative quantity from the data as it is junk
len(transaction)
transaction.head()

##Changing the data column into date format
transaction['Date']=pd.to_datetime(transaction['Date'], format='%m/%d/%Y')
transaction['year']=pd.DatetimeIndex(transaction['Date']).year.astype('str')
transaction['Concat']=transaction['Concat'].astype('str')  #using an alternate date for plotting graphs
len(transaction['Concat'].unique())
transaction.columns

"""<b>Exploratory Data Analysis"""

####Merging all the datasets to form the master table 
df=pd.merge(transaction,customer,how='inner',left_on='cust_id',right_on='customer_Id')
master_df=pd.merge(df,prod_cat,how='left',left_on=['prod_cat_code','prod_subcat_code'],right_on=['prod_cat_code' ,'prod_sub_cat_code'])
master_df['Concat']=master_df['Concat'].astype('str')

master_df.head()

# Checking for null values in the dataframe
len(master_df.isnull().values[master_df.isnull().values==True])
print(f'There are only {len(master_df.isnull().values[master_df.isnull().values==True])} missing values in the dataset')
print('We can also visualize the percentage of missing values this via missing map')


master_df.isnull().sum()

sns.heatmap(master_df.isnull(), cbar=False,cmap=['black','yellow'])
##where the yellow color represent the missing values and the black is where there are some values
##As wecan see they negligible missing values in the dataset and thus can be ignored
master_df.dropna(inplace=True)

master_df.info()

##Creating two additional columns for date##
master_df['Day of Week'] =master_df['Date'].dt.day_name()
master_df['Month'] =master_df['Date'].dt.month

"""<b> Time series trends </b>

<b> Monthly sales Across Time <b>
"""

monthly_df=master_df.groupby(['Concat'])['total_amt'].sum().to_frame().reset_index()
fig, ax = plt.subplots()
fig.set_size_inches(40, 8)
plt.plot('Concat','total_amt',data=monthly_df)
sns.set_style("dark")
plt.xlabel('Months',fontsize=20)
plt.ylabel('Sales (in $)',fontsize=20)
plt.title('Distribution of Sales Across Months',fontsize=20)

"""<b>Monthly sales per store type across time<b>"""

plt.figure(num=None, figsize=(40, 8), dpi=80, facecolor='w', edgecolor='k')
sns.set(style="whitegrid")
fig.set_size_inches(40, 8)
monthlystore_df=master_df.groupby(['Store_type','Concat'])['total_amt'].sum().to_frame().reset_index()
sns.lineplot('Concat','total_amt',data=monthlystore_df,hue='Store_type') 
plt.xlabel('Months',fontsize=20)
plt.ylabel('Sales (in $)',fontsize=20)
plt.title('Total amount through transactions monthly from the start to end for different stores',fontsize=20)
plt.legend(loc='upper left', bbox_to_anchor=(1.03, 1),fontsize=20)

"""It can be seen that total transactions for e-shop is much higher than the other three stores across time while the other three stores

<b> Monthly Analysis  order </b>

<b> Weekly Analysis </b>
"""

plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
sns.set(style="whitegrid")
grouped_values=master_df.groupby(['Day of Week']).count().reset_index()
g=sns.barplot(x='Day of Week',y='transaction_id',data=grouped_values,palette='coolwarm')

plt.title('Transactions per week across all the stores')
for p in g.patches:
  g.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')

"""There is negligible difference between the number of orders per day of the week and almost identical number of orders are sold on each day of the week

Teleshop -to buy goods by telephone or via the internet.

A flagship store is the most important store in a chain, often with the largest volume of sales, or the most up-to-date formats or layouts. It is usual that the opening of a flagship store marks the first development of a retail store portfolio within a luxury fashion retailer's most important foreign markets.

An e-shop is an online business that sells a variety of goods and services. E-shops are business-to-consumer oriented. They are just like a retail store but instead of having a physical location, its location is on the internet

The term "brick-and-mortar" refers to a traditional street-side business that offers products and services to its customers face-to-face in an office or store that the business owns or rents. The local grocery store and the corner bank are examples of brick-and-mortar companies

As seen through the time series data for eachstore E-shop should produce a higher transaction amount as compared to the other three stores ,
lets plot a bar graph to see that
"""

plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('ggplot')
labels = master_df['Store_type'].value_counts().index
sizes = master_df['Store_type'].value_counts().values
explode = (0.1, 0.0, 0.0, 0.1)  # only "explode" the 2nd and 3rd slices (i.e. 'Hogs')
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90 ,colors=colors)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Total unique transactions for different Store Types")

"""We can see that more than <b> 60% </b> of the transactions are for e-shop and Teleshops which indicated the shift in the mindset of people earlier this decade as this was the time when big giants such as Amazon and other E-commerce websites

As we can see that total amount of transactions for E-shop is approximately twice as compared to the other store types

<b> Product Categories </b>
"""

plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('ggplot')
labels = master_df['prod_cat'].value_counts().index
sizes = master_df['prod_cat'].value_counts().values
explode = (0.1, 0.0, 0.0, 0.0,0.0,0.1)  # only "explode" the 2nd and 3rd slices (i.e. 'Hogs')
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','magenta','cyan']
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90 ,colors=colors)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Total unique transactions for different product categories")

"""Books have the highest number of transactions and the second one is electronics , the lowest is bags"""

# master_df.rename(columns={'product_category':'product category', 'total_amt': 'Total sales amount'},inplace=True)
########Purchase behavior by category, age and gender
plt.figure(figsize=(30,10))
sns.set(style="whitegrid")
df2=master_df.groupby(['prod_cat','Age_group','Gender']).sum()['total_amt'].reset_index()
df2.rename(columns={'prod_cat':'product category','total_amt':'Total sales amount'},inplace=True)
g=sns.catplot(x="product category", y="Total sales amount",hue="Age_group", col="Gender",data=df2, kind="bar")
g.set_xticklabels(rotation=30)

plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
sns.set(style="whitegrid")
df2=master_df.groupby(['prod_cat']).sum()['total_amt'].reset_index()
g=sns.barplot(x='prod_cat',y='total_amt',data=df2,palette='viridis')
plt.title('Sales Across all the stores')
for p in g.patches:
  g.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.ylabel("Sales (in $)")

"""An interesting thing to note here is that Books were responsible for the maximum transaction amount even higher than electronics and the lowest conribution is acoounted by bags.

From the above analysis for both the store types and product categories we can see that the number of unique transactions are positevely correlated to the amount of transaction produced , which is kind of expected

<b>Distribution of transactions amounts
"""

enable_plotly_in_cell()
master_df['total_amt'].iplot(kind='hist',bins=25)

"""<b> Correlation plot </b>

<b>Gender and age analyisis<b>
"""

# master_df['DOB'] = master_df['DOB'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y') if '-' in x else datetime.strptime(x, '%d/%m/%Y'))
master_df['DOB'] = pd.to_datetime(master_df['DOB'], format = '%m/%d/%Y')
master_df['Age']=master_df['Date']-master_df['DOB']
master_df['Age']=master_df['Age'].apply(lambda x:round(int(str(x).split()[0])/365,0))
master_df['Age_group']=master_df['Age'].apply(lambda x: 'Young' if (18<=x<=25) else ('Middle' if (25<x<=35) else 'Old'))

plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
Gender_count=master_df.groupby(['Gender'])['customer_Id'].nunique().to_frame().reset_index()

plt.pie(Gender_count['customer_Id'],labels=Gender_count['Gender'],autopct='%1.1f%%')
plt.title("Distribution of Males and Females visiting the retail store")
plt.axis('equal') 
plt.show()

"""There are more male customers then female customers but the ratio is not different"""

#####Removing the 2014 data due to its discrepancy
master_df_sub=master_df[master_df['Date']<='2013-12-31']

"""<b>Problem1 - Customer Segmentation"""

######Clustering approach
df3_clustering=master_df_sub.groupby('cust_id').agg({'total_amt':'sum','Qty':'sum','transaction_id':'nunique','Age':'mean'}).reset_index()
df3_clustering['Sales/Trans']=df3_clustering['total_amt']/df3_clustering['transaction_id']
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
# scaler.fit(df3_clustering[["Sales/Trans","Qty","Age"]])
# x=scaler.transform(df3_clustering[["Sales/Trans","Qty","transaction_id"]])
x=scaler.fit_transform(df3_clustering[["Sales/Trans","Qty","transaction_id"]])  ###Scaling all variables to treat all the importance equally
x=pd.DataFrame(x)
cluster_results=x
x

from sklearn.cluster import KMeans
# Empty list to store Sum of squared distances of samples to their closest cluster centre
inertias = []
for k in range(1,10):
    # Create a KMeans instance with k clusters: model
    model = KMeans(n_clusters=k)
    # Fit model to samples
    #model.fit(pca_1.iloc[:,:3])
    model.fit(cluster_results)
    # Append the inertia to the list of inertias
    inertias.append(model.inertia_)
plt.plot(range(1,10), inertias, '-o', color='black')
plt.xlabel('Number of clusters, k')
plt.ylabel('inertia')
plt.title('Elbow curve to choose the optimum #Clusters')
plt.xticks(range(1,10))
plt.show()

###Fitting the algorithm to the data
kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10, random_state=0)
pred_y = kmeans.fit_predict(cluster_results)
pred_y=pd.DataFrame(pred_y,columns=['Cluster'])
df3_clustering1 = pd.concat([df3_clustering,pred_y], axis=1)
# df3_clustering1=pd.merge(master_df,df3_clustering1,left_on='customer_Id',right_on='cust_id',how='left')
kmeans.cluster_centers_

############Saving the results in a file###################
df3_clustering1.to_excel("cluster_results2.xlsx")

#######3D package imported######
from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure(figsize=(15,8))
# ax = fig.add_subplot(111, projection='3d')
# x=['yellowgreen', 'gold', 'lightskyblue']
# for i,num in enumerate(x):
#   plt.scatter(df3_clustering1[df3_clustering1["Cluster"]==i]["total_amt_x"],df3_clustering1[df3_clustering1["Cluster"]==i]["Qty_x"],df3_clustering1[df3_clustering1["Cluster"]==i]["transaction_id_x"],label='Cluster'+str(i), c =num)
#   plt.legend(loc='upper left')
# ax.set_xlabel('Total Amount')
# ax.set_ylabel('Quantity')
# ax.set_zlabel('Number of Transactions')
# plt.legend(loc='upper left', bbox_to_anchor=(1.03, 1))
# plt.title('K-mean clustering for customer segementation : K=3')
# plt.tight_layout()

df3_clustering1.head()

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection="3d")

plt.show()

fig = plt.figure()
ax = plt.axes(projection="3d")

z_line = np.linspace(0, 15, 1000)
x_line = np.cos(z_line)
y_line = np.sin(z_line)
ax.plot3D(x_line, y_line, z_line, 'gray')

z_points = df3_clustering1['Qty']
x_points = df3_clustering1['Sales/Trans']
y_points = df3_clustering1['Age']
ax.scatter3D(x_points, y_points, z_points, c=z_points);

plt.show()

##########3D view of the clusters############
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df3_clustering1["Sales/Trans"],df3_clustering1["Qty"],df3_clustering1["transaction_id"], 
            c=df3_clustering1['Cluster'], cmap='viridis',
            edgecolor='k', s=40, alpha = 0.5)
ax.set_xlabel('Sales/Transaction')
ax.set_ylabel('Qty')
ax.set_zlabel('No. of transactions')
ax.set_title('3 Dimmensional plot for Retail dataset (K-means clustering)')
plt.tight_layout()

#######Interactive view to get cluster view - Rotate to get a better picture#######
enable_plotly_in_cell()
import plotly.express as px
df = df3_clustering1
df=df.rename(columns={'transaction_id': '#transactions'})
# df=df.rename(columns={'', 'Transactions'})
df.head()
fig = px.scatter_3d(df, x='Sales/Trans', y='Qty', z='#transactions',
             color='Cluster', opacity=0.2)

fig.show()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# scatter = ax.scatter(df3_clustering1["Sales/Trans"],df3_clustering1["total_amt"],
#                      c=df3_clustering1['Cluster'],s=50)
# ax.set_title('K-Means Clustering')
# ax.set_xlabel('GDP per Capita')
# ax.set_ylabel('Corruption')
# plt.colorbar(scatter)

"""<b>Problem2 - Sales Forecasting"""

####code for forecasting###############################
master_df.head()

master_df['total_amt']=winsorize(master_df['total_amt'], limits=0.05)
master_df['Qty']=winsorize(master_df['Qty'], limits=0.1)
master_df['Week']=master_df['Date'].dt.week
master_df['Year']=master_df['Date'].dt.year
master_df['Week_no']=np.where(master_df['Week']<10,master_df['Year'].astype('str')+"0"+master_df['Week'].astype('str'),master_df['Year'].astype('str')+master_df['Week'].astype('str'))

###############Aggregating the data at a weekly level######
master_df1=master_df.groupby(['Week_no','Concat']).agg({'total_amt':'sum','Qty':'sum','transaction_id':'nunique','customer_Id':'nunique'}).reset_index().sort_values(by='Concat')
master_df1['Concat']=master_df1['Concat'].astype('int')

# master_df1['eshop_sales']=master_df.groupby('Concat').apply(lambda x : x['total_amt'][x['Store_type']=='e-Shop'].sum()).reset_index(level=0,drop=True)
# master_df1['eshop_trans']=master_df.groupby('Concat').apply(lambda x : x['transaction_id'][x['Store_type']=='e-Shop'].nunique()).reset_index(level=0,drop=True)
master_df1=master_df1[master_df1['Concat']<=201312]
master_df1

##################Training and Testing###############
X_train=master_df1[master_df1['Concat']<=201304].drop(columns=['total_amt','Concat','Week_no'])
y_train=master_df1[master_df1['Concat']<=201304]['total_amt']
X_test=master_df1[master_df1['Concat']>201304].drop(columns=['total_amt','Concat','Week_no'])
y_test=master_df1[master_df1['Concat']>201304]['total_amt']

#############Importing packages##############
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn import metrics

###########Fitting linear regression and calculating respective metrics in the following code#################
regressor = LinearRegression()  
regressor.fit(X_train, y_train)

print(regressor.intercept_)

print(regressor.coef_)

regressor.score(X_train, y_train)

y_pred = regressor.predict(X_test)

# df = pd.DataFrame({'Actual': Y_test.flatten(), 'Predicted': y_pred.flatten()})
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred)) 
print('Mean Absolute Error:', metrics.mean_squared_error(y_test, y_pred)) 
print("The mean absolute % error is {}%".format(round(np.mean(np.abs(y_pred- y_test.values)/np.abs(y_test.values))*100,2)))

r2_score(y_test, y_pred)

coeff_df = pd.DataFrame(regressor.coef_, X_train.columns, columns=['Coefficient'])  
coeff_df

#############Building a correlation matrix###############
master_df1.rename(columns={'transaction_id':'total_transactions','customer_Id':'total_customers'},inplace=True)
master_df1.corr()
corr = master_df1.drop(columns=['Concat']).corr()
corr.style.background_gradient(cmap='coolwarm')

"""#############We cant use linear regression for this data as it doesn't satisfy any linear assumption:
The dependent variable is not normally distributed
The autocorrelation would exist in a time series while it is 0 in LinearRegression

Time series modelling
"""

master_df1['Week_no']=master_df1['Week_no'].astype(str)
master_df1.dtypes

###########Distribution of sales across weeks till 2013#
master_df1=master_df[master_df['Date']<='2013-12-31']
master_df1=master_df1[master_df1['Date']!='2011-01-02']
weekly_df=master_df1.groupby(['Week_no'])['total_amt'].sum().to_frame().reset_index().sort_values(by='Week_no')
weekly_df['Week_no']=weekly_df['Week_no'].astype(str)
fig, ax = plt.subplots()
fig.set_size_inches(60, 8)
plt.plot('Week_no','total_amt',data=weekly_df)
sns.set_style("dark")
plt.xlabel('Weeks',fontsize=20)
plt.ylabel('Sales (in $)',fontsize=20)
plt.title('Distribution of Sales Across Months',fontsize=20)

weekly_df.head(60)

##########Decomposing the time series into trend, seasonality and cycles
from random import randrange
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose
series = weekly_df['total_amt']
result = seasonal_decompose(series, model='additive', freq=52)
result.plot()
pyplot.show()

"""<b>We need to find the if the time series in stationary
We formulate an hypothesis and check for its stationarity for a significance level of 0.05 using dicky fuller test<br>
NULL: The sales data is not stationary<br>
Aternate: The sales data is stationary
"""

from statsmodels.tsa.stattools import adfuller
from numpy import log
result = adfuller(weekly_df.total_amt.dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

"""By looking at the p value, we reject the NULL hyothesis and it implies we dont need to difference the series as it is already stationary"""

# PACF plot of 1st differenced series
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plt.rcParams.update({'figure.figsize':(9,3), 'figure.dpi':120})


# fig, axes = plt.subplots(1, 2, sharex=True)
# axes[0].plot(weekly_df.total_amt.diff()); axes[0].set_title('1st Differencing')
# # axes[1].set(ylim=(0,5))
plot_pacf(weekly_df.total_amt.dropna())
plt.xlabel('AR Lag')
plt.ylabel('Strength/Correlation')
plot_acf(weekly_df.total_amt.dropna())
plt.xlabel('MA Lag')
plt.ylabel('Strength/Correlation')


plt.show()

########Fitting the ARIMA model with the obtained parameters from the plots
from statsmodels.tsa.arima_model import ARIMA

# 1,1,2 ARIMA Model
model = ARIMA(weekly_df.total_amt, order=(4,0,3))
model_fit = model.fit(disp=0)
print(model_fit.summary())

residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()

model_fit.plot_predict(dynamic=False)
plt.show()

from statsmodels.tsa.stattools import acf

# Create Training and Testing set
X_train = weekly_df.total_amt[:126]
X_test = weekly_df.total_amt[126:]

# Build Model

model = ARIMA(X_train, order=(3, 0, 4))  
fitted = model.fit(disp=-1) 
print(fitted.summary())

# Forecast
fc, se, conf = fitted.forecast(29, alpha=0.1)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc, index=X_test.index)
lower_series = pd.Series(conf[:, 0], index=X_test.index)
upper_series = pd.Series(conf[:, 1], index=X_test.index)

# Plot
plt.figure(figsize=(12,5), dpi=100)
plt.plot(X_train, label='training')
plt.plot(X_test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series, 
                 color='k', alpha=.1)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()

############Calculating the MAPE of the model############
pd.DataFrame([fc_series,X_test])
dataset = pd.DataFrame({'test_set': X_test,'forecast': fc_series})
dataset['PE']=(abs(dataset['test_set']-dataset['forecast'])/dataset['test_set'])

print("The mean absolute % error is {}%".format(round(np.mean(np.abs(fc- X_test.values)/np.abs(X_test.values))*100,2)))
print("The mean % error is {}%".format(round(np.mean((fc- X_test.values)/(X_test.values))*100,2)))

X=weekly_df.reset_index()['index']
y=weekly_df['total_amt']

"""<b>Doing cross validation using TimeSeriesSplit that can take care of the ordering data when splitting it"""

from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit()
print(tscv)
TimeSeriesSplit(max_train_size=130, n_splits=5)
z=0
for train_index, test_index in tscv.split(X):
  print("TRAIN:", train_index, "TEST:", test_index)
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]
  try:
    model = ARIMA(y_train, order=(3, 0, 4))
    fitted = model.fit(disp=-1) 
  except: 
    pass
  fc, se, conf = fitted.forecast(25, alpha=0.1)
  print(fc.shape)
  print(y_test.shape)
  mape=np.mean(np.abs(fc- y_test.values)/np.abs(y_test.values))*100  
  z=(mape+z)/2
  print(z)

print("The average MAPE of the model comes out to be {}".format(round(z,3))+"%")

####installing pmdarima for paramter tuning and estimation###
!pip install pmdarima

# Create Training and Testing set
X_train = weekly_df.total_amt[:126]
X_test = weekly_df.total_amt[126:]
X_train

########The autoarima model takes the seasonal component (Seasonal=True) into account and finds the best parameters
import pmdarima as pm
smodel = pm.auto_arima(X_train, start_p=1, start_q=1,
                         test='adf',
                         max_p=3, max_q=3, m=52,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)

smodel.summary()

# data = X_train
# obtained model configurations
my_order = (3, 1, 0) 
# my_seasonal_order = (1, 1, 0, 52)
import statsmodels.api as sm
# define model
model = sm.tsa.statespace.SARIMAX(endog=X_train, order=my_order,seasonal_order=(1,1,0,52),enforce_stationarity=True,enforce_invertibility=True)
# ,seasonal_order=my_seasonal_order)

res = model.fit(disp=False)
print(res.summary())

##plots to analyze additional results
res.plot_diagnostics(figsize=(18, 8))
plt.show()

########Calculating the MAPE for single model run
X = res.predict(start = 126, end= 154, dynamic= True)
df = pd.DataFrame({'Actual': weekly_df.total_amt, 'Predicted': X})
df[['Actual', 'Predicted']].plot(figsize=(12, 8))
plt.xlabel('Weeks')
plt.ylabel('Sales (in $)')
np.mean(abs(df.dropna()['Actual']-df.dropna()['Predicted'])/df.dropna()['Actual'])

"""<b>Cross Validation run for testing the robusticity of a model"""

# Create Training and Testing set
X=weekly_df['total_amt']

from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit()
print(tscv)
TimeSeriesSplit(max_train_size=130, n_splits=5)
z=[]
for train_index, test_index in tscv.split(X):
  print("TRAIN:", train_index, "TEST:", test_index)
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]
  try:
    smodel = pm.auto_arima(y_train, start_p=1, start_q=1,
                         test='adf',
                         max_p=3, max_q=3, m=52,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)
    fitted = smodel.fit(disp=-1) 
  except: 
    pass
    fc, se, conf = fitted.forecast(25, alpha=0.1)
    # fc = fitted.forecast(25, alpha=0.1)
    # print(fc.shape)
    print(y_test.shape)
    mape=np.mean(np.abs(fc- y_test.values)/np.abs(y_test.values))*100  
    z.append(mape)
    print(z)

x=sum(z)/len(z)
print("The average MAPE of the model comes out to be {}".format(round(x,3))+"%")

"""**Problem3 - Customer Product Affinity**

"""

master_df.groupby(['cust_id'])['prod_subcat'].nunique().to_frame()

#########Find the share of total amount spent on each sub category by each customer
prod_aff=master_df.groupby(['cust_id','prod_subcat'])['total_amt'].sum().to_frame().reset_index()
prod_aff=prod_aff.pivot(index='cust_id',columns='prod_subcat',values='total_amt')
prod_aff.fillna(0,inplace=True)
prod_aff=pd.merge(prod_aff,df3_clustering1[['cust_id','Cluster','transaction_id','total_amt']],how='inner',on=['cust_id','cust_id'])
prod_aff

## Find the top1, top2 and top3 sub category for each customer
df_1=prod_aff.drop(columns=['cust_id','Cluster','transaction_id','total_amt'],axis=1)
result1=prod_aff[['cust_id','Cluster']]
# df_1.drop(columns=['max1','max2','max3'],axis=1,inplace=True)
len(df_1.columns)
df_1['id'] = range(len(df_1))
df_1 = df_1.set_index('id')
nlargest = 3
df_1.head()
order = np.argsort(-df_1.values, axis=1)[:, :nlargest]
result = pd.DataFrame(df_1.columns[order], 
                      columns=['top{}'.format(i) for i in range(1, nlargest+1)],
                      index=df_1.index)
prod_aff_cluster=pd.concat([result1,result],axis=1)
prod_aff_cluster.head()
# prod_aff_cluster.to_csv("y.csv")

# prod_aff['max1'] = prod_aff.drop(columns=['cust_id','Cluster']).T.apply(lambda x: x.nlargest(1).idxmin())
# prod_aff['max2'] = prod_aff.drop(columns=['cust_id','Cluster','max1']).T.apply(lambda x: x.nlargest(2).idxmin())
# prod_aff['max3'] = prod_aff.drop(columns=['cust_id','Cluster','max1','max2']).T.apply(lambda x: x.nlargest(3).idxmin())
prod_aff

#Filtering the customers according to the cluster they belong to#######
prod_aff_cluster.head()
prod_aff_cluster_0=prod_aff_cluster[prod_aff_cluster['Cluster']==0]
prod_aff_cluster_1=prod_aff_cluster[prod_aff_cluster['Cluster']==1]
prod_aff_cluster_2=prod_aff_cluster[prod_aff_cluster['Cluster']==2]

"""<b> Analysing product suggestions according to different clusters </b>"""

# # Rectifiying max 2 and max 3 error - code by Gopu Panda boy 
# df_1=prod_aff.drop(columns=['cust_id','Cluster','total_amt','transaction_id'],axis=1)
# # df_1.drop(columns=['max1','max2','max3'],axis=1,inplace=True)
# len(df_1.columns)
# df_1['id'] = range(len(df_1))
# df_1 = df_1.set_index('id')
# nlargest = 3
# df_1.head()
# order = np.argsort(-df_1.values, axis=1)[:, :nlargest]
# result = pd.DataFrame(df_1.columns[order], 
#                       columns=['top{}'.format(i) for i in range(1, nlargest+1)],
#                       index=df_1.index)
# result
# prod_aff_cluster=pd.concat([result1,result],axis=1)
# prod_aff_cluster.head()

##########User defined funtion to concatenate all the top1,2,3 products to get the purchase chain
def product_affinity(x,y):
  """
  :param - x : a dictionary to store product affinity information
  :param - y : a datframe containing top three max sequences
  :returns : x
  
  """
  for i,j,k in zip(list(y['top1']),list(y['top2']),list(y['top3'])):
    if i + " " + j + " " + k in x.keys():
      x[i + " " + j + " " + k]+=1
    else:
      x[i + " " + j + " " + k]=1
  x=sorted(x.items(),key=lambda item:item[1], reverse=True)
  x=pd.DataFrame(x[0:20])
  x.rename(columns={1:'#Customers', 0:'most prominent sequence'},inplace=True)
  return x

"""<B> Cluster 0 </B>"""

plt.figure(figsize=(12,6))
suggestions_0={}
suggestions_0=product_affinity(x=suggestions_0,y=prod_aff_cluster_0)
enable_plotly_in_cell()
g=sns.barplot(x='most prominent sequence',y='#Customers',data=suggestions_0)
plt.style.use('Solarize_Light2')
g.set_xticklabels(g.get_xticklabels(),rotation=90)
plt.title('Product sequence suggestions for cluster 0 population')

"""<B> Cluster 1 </B>"""

suggestions_0.head()

plt.figure(figsize=(12,6))
suggestions_1={}
suggestions_1=product_affinity(x=suggestions_1,y=prod_aff_cluster_1)
enable_plotly_in_cell()
g=sns.barplot(x='most prominent sequence',y='#Customers',data=suggestions_1,palette='coolwarm')
plt.style.use('Solarize_Light2')
g.set_xticklabels(g.get_xticklabels(),rotation=90)
plt.title('Product sequence suggestions for cluster 1 population')

"""<b> Cluster 2 </b>"""

plt.figure(figsize=(12,6))
suggestions_2={}
suggestions_2=product_affinity(x=suggestions_2,y=prod_aff_cluster_2)
enable_plotly_in_cell()
g=sns.barplot(x='most prominent sequence',y='#Customers',data=suggestions_2,palette='plasma')
plt.style.use('Solarize_Light2')
g.set_xticklabels(g.get_xticklabels(),rotation=90)
plt.title('Product sequence suggestions for cluster 2 population')

prod_aff_cluster['concat']=prod_aff_cluster['top1']+"-"+prod_aff_cluster['top2']+"-"+prod_aff_cluster['top3']

final=pd.merge(prod_aff,prod_aff_cluster,on=['cust_id','cust_id'],how='left')
final.head()

#######To check if the clusters are different using ks sample test. Rejecting the hypothesis confirms that they are different
from scipy import stats
print(stats.ks_2samp(np.array(final[final['Cluster_x']==0]['transaction_id']),np.array(final[final['Cluster_x']==1]['transaction_id'])))
print(stats.ks_2samp(np.array(final[final['Cluster_x']==1]['transaction_id']),np.array(final[final['Cluster_x']==2]['transaction_id'])))
print(stats.ks_2samp(np.array(final[final['Cluster_x']==0]['transaction_id']),np.array(final[final['Cluster_x']==2]['transaction_id'])))

import sys
sys.version

