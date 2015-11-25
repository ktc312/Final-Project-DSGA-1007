__author__ = 'ktc312'


'''
read data
descriptive statistics & Scatter
forcasting
'''

def user_input():
	currency = user_choose_stock
	analyzedate = star_and_end_date
	#use raw input first and when we build the GUI, change it into drop-down list input
	return currency,analyzedate

def read_data():
	data = read_the data_from_yahoo(currency)
	slicing_data = sliceing_by_analyzedate(data,analyzedate)
	return slicing_data

def sliceing_by_analyzedate(data,star_and_end_date):
	#sliceing_by_analyzedate
	return sliced_data

class descriptive:
	def __init__(self):
		pass
	def mean(self):
		pass
	def mode(self):
		pass
	def medium(self):
		pass
	def std(self):
		pass
	def scatter(self):
		# draw scatter plot
		passs

	# and any other descriptive statistics

class Model_Train:
    # Deciding parameters: (a) when d=0,1,2, acf and pacf computing (& plot);
	# (b)Tell which d’s acf and pacf are best, then get the parameter d.
	# (c) AICC computing (use d to get p, q)
	# Arima forecasting using the model (get the forecasting values) and plot
	def __init__(self, dataframe):
        '''take dataframe as input'''
        pass

    def build_arma_model(self):
        '''this function should take a dataframe as input then build a arma_model and train
        it with data. Returns a trained arma_model'''
        pass

    def train_model_metrics(self):
        ''' calculates referenced metrics for the model, such as acf, pacf, pavales,
        Q-statistics, etc. Should return a summary dataframe of the metrics. '''
        pass

    def model_parameters(self):
        ''' returns parameters for the optimal model'''
        pass

class Arma_Model:
    def __init__(self, dataframe, parameters):
        '''take dataframe as input'''
        pass

    def apply_arma_model(self):
        '''this function will use the model created in the Model_Train class to predict
        future data.'''
        pass

def out_put:
    #print all the results in the class above first, we can do something else when we start building GUI