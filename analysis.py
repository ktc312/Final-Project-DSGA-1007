__author__ = 'liz'

from yahoo_finance import Share
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from scipy import stats
import matplotlib.pyplot as plt
import scikits.statsmodels.api as sm
import scikits.statsmodels.tsa.arima_process as tsp
import scikits.statsmodels.tsa.stattools as tss
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA

class Analysis:
    '''class which deals with all the analytical procedures'''

    def __init__(self, start_date, end_date, ticker):
        '''clean data and store class attributes'''
        stock = Share(ticker)
        df = pd.DataFrame(stock.get_historical(start_date,end_date))[['Date','Adj_Close']]
        df['Adj_Close'] = df['Adj_Close'].astype(float)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_index(by = 'Date', ascending = True)
        df.index = range(len(df))
        df.columns = ['Date', 'Price']
        self.df = df
        self.ts = df.set_index('Date')
        self.date = df['Date']
        self.val = df['Price']
        self.start = self.ts.index[0]
        self.end = self.ts.index[-1]
        self.diff1_val = pd.Series(np.diff(self.val))
        self.diff1_val_na = pd.Series(np.concatenate(([np.nan], self.diff1_val.values)))
        self.diff2_val = pd.Series(np.diff(self.diff1_val_na))
        self.diff2_val_na = pd.Series(np.concatenate(([np.nan], self.diff2_val.values)))

    def descriptive_stat(self):
        '''function shows basic decriptive stats about the timeseries data, returns statistics in an array'''
        return self.df.describe().values

    def orig_data_plot(self):
        '''plot original timeseries plot'''
        plt.plot(self.date, self.val)
        plt.savefig('origianl time series data plot.jpg')
        plt.clf()

    def d_param(self, diff):
        '''function takes different values for difference step, and returns true or false flag if acf and pacf values
        lie into the threshold area'''
        THRESHOLD = 0.08
        if diff == 0:
            acf = tss.acf(self.val)
            pacf = tss.pacf(self.val)
            # check save fig for acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.val,lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig= plot_pacf(self.val, lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF.jpg')
            plt.close()
            # check for optimal parameter d
            acf_percent = len(acf[np.abs(acf) <= THRESHOLD])/float(len(acf))
            pacf_percent = len(pacf[np.abs(pacf) <= THRESHOLD])/float(len(pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        elif diff == 1:
            diff1_acf = tss.acf(self.diff1_val.dropna())
            diff1_pacf = tss.pacf(self.diff1_val.dropna())
            # check save fig for acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.diff1_val.dropna(),lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig= plot_pacf(self.diff1_val.dropna(), lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF_diff1.jpg')
            plt.close()
            acf_percent = len(diff1_acf[np.abs(diff1_acf) <= THRESHOLD])/float(len(diff1_acf))
            pacf_percent = len(diff1_pacf[np.abs(diff1_pacf) <= THRESHOLD])/float(len(diff1_pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        elif diff == 2:
            diff2_acf = tss.acf(self.diff2_val.dropna())
            diff2_pacf = tss.pacf(self.diff2_val.dropna())
            # check save fig for acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.diff2_val.dropna(),lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig = plot_pacf(self.diff2_val.dropna(), lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF_diff2.jpg')
            plt.close()
            acf_percent = len(diff2_acf[np.abs(diff2_acf) <= THRESHOLD])/float(len(diff2_acf))
            pacf_percent = len(diff2_pacf[np.abs(diff2_pacf) <= THRESHOLD])/float(len(diff2_pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        else:
            print "d only takes [0,1,2]"

    def d_determination(self):
        '''fuction which determines the value for d (distancing)'''
        if self.d_param(0):
            return 0
        elif self.d_param(1):
            return 1
        elif self.d_param(2):
            return 2
        else:
            # print "Couldn't get a best diff model, so we use diff1 model"
            return 1

    def param_dict(self):
        '''build a dictionary to map param orders to aics'''
        d = self.d_determination()
        if d == 0:
            ts = self.ts
        elif d == 1:
            dic = {'Date' :self.date, 'diff1_val': self.diff1_val_na}
            df_new =pd.DataFrame(dic)
            ts = df_new.set_index('Date')
        else:
            dic = {'Date' :self.date, 'diff2_val': self.diff2_val_na}
            df_new =pd.DataFrame(dic)
            ts = df_new.set_index('Date')
        arima_mod_aics = {}
        for p in range(3):
            for q in range(3):
                try:
                    order = (p, 0, q)
                    params = (p, d, q)
                    arima_mod = ARIMA(ts.dropna(), order).fit(method = 'css-mle', disp = 0)
                    arima_mod_aics[params] = arima_mod.aic
                except:
                    pass
        return arima_mod_aics

    def param_df(self):
        '''return a dataframe built from the arima_mod_aics'''
        self.aic_df = pd.DataFrame(self.param_dict().items(), columns = ['param order', 'aic'])
        return self.aic_df

    def param_determination(self):
        '''funtion which determines values for parameter's p (autoregressive) and q (moving average)
        based on value of d, returns final parameter order in a tuple'''
        arima_mod_aics = self.param_dict()
        for param, aic in arima_mod_aics.items():
            if aic == min(arima_mod_aics.values()):
                return param

    def arima_model(self):
        ''' uses parameter order determined in param_determination() to fit an ARIMA model, returns model results'''
        order = self.param_determination()
        self.results = ARIMA(self.ts, order).fit(method = 'css-mle', disp = 0 )
        return self.results

    def predict_val(self):
        '''using arima model to forecast the stock values in the next 7 days'''
        self.pred_val = self.arima_model().forecast(7)[0]
        base = self.end
        self.time_period = [base + timedelta(days = x) for x in range(1,8)]
        pred_df =  pd.DataFrame(self.pred_val, index = self.time_period)
        pred_df.columns = ['Price']
        return pred_df

    def compare_plot(self):
        '''generate comparison plot'''
        result = self.arima_model()
        fig = result.plot_predict()
        plt.savefig('Predicted_vs_historical_data.jpg')

    def predict_plot(self):
        '''generate prediction plot'''
        # frames = [self.ts, self.predict_val]
        # result = pd.concate(frames)
        pred_df =  self.predict_val()
        pred_df.ix[self.end] = self.val[len(self.df)-1]
        pred_df = pred_df.sort_index(ascending = True)
        pred_time = pred_df.index
        pred_vals = pred_df['Price']
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.plot(self.date, self.val, '-b', label = 'original data')
        ax1.plot(pred_time, pred_vals, '-r', label = 'predicted values')
        ax1.set_title('Full plot')

        base = self.ts.index[-60]
        ax2 = fig.add_subplot(212)
        ax2.plot(self.ts.index[-60:], self.ts.Price[-60:], '-b', label = 'original data')
        # ax2.plot(self.date, self.val, '-b', label = 'original data')
        ax2.plot(pred_time, pred_vals,'+r',label = 'predicted values' )
        # ax2.xticks([base + timedelta(days = x) for x in range(0, 90, 10)], rotation = 90)
        ax2.set_title('Close-up plot')
        plt.savefig('Predicted_plots.jpg')




















