__author__ = 'ktc312'

from yahoo_finance import Share
import pandas as pd


start_date = '2010-01-01'
end_date = '2015-11-24'
yahoo = Share('YHOO')

df = pd.DataFrame(yahoo.get_historical(start_date,end_date ))

