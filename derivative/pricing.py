# TODO: add underlying stock dividend component into valuation model
from math import exp, sqrt

def getQ(N, T, up_rate, volatility, risk_free_rate, dividend, black_scholes=False):
    if black_scholes == False:
        up = 1 + up_rate
        down = 1/float(up)
        q = ((1+risk_free_rate-dividend)-down)/float(up-down)
    elif black_scholes == True:
        up = exp(volatility * sqrt(T/float(N)))
        down = 1/float(up)
        q = (exp((risk_free_rate-dividend)*T/float(N))-down)/(float(up-down))
    else:
        raise ValueError("Please input boolean value!")
    print(up, down, q)
    return up, down, q

def getSingleValue(N, T, product, risk_free_rate, up_value, down_value, q, black_scholes, option_value=0.0):
    if black_scholes == False and product.product == "Options":
        value = 1/float(1+risk_free_rate) * (q * up_value +(1-q) * down_value)
    elif black_scholes == True and product.product == "Options":
        value = exp(-risk_free_rate*T/float(N)) * (q * up_value +(1-q) * down_value)
    else:
        value = (q * up_value +(1-q) * down_value)
    if product.type == "American":
        value = max(value, option_value)
    return value

def singlePeriodModelValuation(N, T, product, up_rate, risk_free_rate, black_scholes):
    up, down, q = getQ(N, T, up, down, risk_free_rate, dividend=0.0, black_scholes=black_scholes)
	
    if product.product == "Options":
        C_u = max((product.spot_price_initial * (up) - product.strike_price)*product.type_boolean,0)
        C_d = max((product.spot_price_initial * (down) - product.strike_price)*product.type_boolean,0)
        shares = (product.spot_price_initial*up - product.strike_price) / float(product.spot_price_initial*(up-down))
	
    elif product.product in ("Forwards", "Futures"):
        C_u = product.spot_price_initial * (up)
        C_u = product.spot_price_initial * (down)
        shares = (product.spot_price_initial*up) / float(product.spot_price_initial*(up-down))
		
    value = getSingleValue(N, T, product, risk_free_rate, C_u, C_d, q, black_scholes=black_scholes) #TODO
    invest_amt = -product.spot_price_initial*down*shares / float(1+risk_free_rate)
    return value, shares, invest_amt


def slideWindow(arr):
    new_arr = list()
    for i in range(len(arr)-1):
        new_arr.append([arr[i],arr[i+1]])
    return new_arr

def getMultipleValue(iter, N, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, idx, acc_outcomes, underlying_value=None, underlying_value_list=None, early_exercise_N=0):
    early_exercise = False
    if iter == 0:
        print("Value at time = " + str(iter) +":\n"+ str(underlying_value))
        if early_exercise_N == 0: early_exercise_N = N
        if product.type == "American": print("Option can be early exercised in time:", early_exercise_N)
        return list(reversed(acc_outcomes))
    else:
        if underlying_value_list is None:
            if product.product == "Options":
                underlying_value = [max((product.spot_price_initial*pow(up,product.N-i)*pow(down,i) - product.strike_price)*product.type_boolean,0) for i in range(0,N+1)]
            elif product.product in ("Forwards", "Futures"):
                underlying_value = [(product.spot_price_initial*pow(up,product.N-i)*pow(down,i)) for i in range(0,product.N+1)]
            underlying_value_list = underlying_value
        elif underlying_value is None:
            underlying_value = [max(v-product.strike_price,0) for v in underlying_value_list[product.N]]
        
        new_outcomes = list()
        acc_outcomes.append(new_outcomes)
        for j in range(iter):
            if product.product == "Options" and underlying.product != "Options":
                option_value = max((underlying_value_list[iter-1][j] - product.strike_price)*product.type_boolean,0)
            elif underlying.product == "Options": option_value = max((product.spot_price_initial*pow(up,iter-j-1)*pow(down,j) - product.strike_price)*product.type_boolean,0)
            else: option_value = 0
            value = getSingleValue(N, T, product, up_value=underlying_value[idx[j][0]], down_value=underlying_value[idx[j][1]], q=q, risk_free_rate=risk_free_rate, black_scholes=black_scholes, option_value=option_value)
            new_outcomes.append(value)
            if value == option_value and value !=0: early_exercise = True or early_exercise
        new_idx = slideWindow(list(range(iter)))
        if early_exercise == True: early_exercise_N = iter-1
        print("Value at time = " + str(iter) +":\n"+ str(underlying_value))
        return getMultipleValue(iter-1, N, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, new_idx, acc_outcomes, new_outcomes, underlying_value_list, early_exercise_N=early_exercise_N)

def multiPeriodModelValuation(T, product, up_rate, risk_free_rate, underlying=None, black_scholes=False, underlying_value_list=None, discount_period=None):
    if discount_period is None: discount_period = product.N
    if underlying is None: underlying = product
    print("Evaluating the "+ product.product + ":")
    up, down, dummy = getQ(underlying.N, T, up_rate, underlying.volatility, risk_free_rate, dividend=underlying.dividend, black_scholes=black_scholes)
    dummy, dummy, q = getQ(discount_period, T, up_rate, product.volatility, risk_free_rate, dividend=product.dividend, black_scholes=black_scholes)
    up_value = 0.0
    down_value = 0.0
	
    idx = slideWindow(list(range(product.N+1)))
    value = getMultipleValue(product.N, discount_period, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, idx, acc_outcomes=list(), underlying_value=None, underlying_value_list=underlying_value_list, early_exercise_N=0)
    return value


