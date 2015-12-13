from analysis import *
import numpy as np
# if start_date = '2014-01-01'
# end_date = '2015-11-24'
# ticker = 'YHOO'
# will have some error
# /Library/Python/2.7/site-packages/statsmodels/base/model.py:466: ConvergenceWarning: Maximum Likelihood optimization failed to converge. Check mle_retvals
#   "Check mle_retvals", ConvergenceWarning)
# /Library/Python/2.7/site-packages/statsmodels/base/model.py:466: ConvergenceWarning: Maximum Likelihood optimization failed to converge. Check mle_retvals
#   "Check mle_retvals", ConvergenceWarning)

start_date = '2010-01-01'
end_date = '2015-11-24'
ticker = 'YHOO'

analysis  = Analysis(start_date, end_date, ticker)
a = analysis.descriptive_stat()
print type(analysis.descriptive_stat()[0])
print str(analysis.descriptive_stat()[0]).replace('[','').replace(']','')
print np.array_str(analysis.descriptive_stat()[0])


# count    500.000000
# mean      -0.039663
# std        1.069371
# min       -3.463789
# 25%       -0.731101
# 50%       -0.058918
# 75%        0.672758
# max        3.120271

