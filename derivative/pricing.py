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

    return up, down, q

def getSingleValue(N, T, product, underlying, risk_free_rate, up_value, down_value, q, black_scholes, option_value=0.0, override_value=None, coupon_payment=None, spot_rate=None):
    if black_scholes == False and product.product == "Options" and underlying.product in ("Stocks", "Futures", "Options"):
        value = 1/float(1+risk_free_rate) * (q * up_value +(1-q) * down_value)
    elif black_scholes == True and product.product == "Options" and underlying.product in ("Stocks", "Futures", "Options"):
        value = exp(-risk_free_rate*T/float(N)) * (q * up_value +(1-q) * down_value)
    elif product.product in ("Rates", "Stocks"):
        value = override_value
    elif product.product == "Bonds":
        value = coupon_payment +  1/float(1+spot_rate) * (q * up_value +(1-q) * down_value)
    elif product.product == "Forwards" and underlying.product == "Bonds":
        value = 1/float(1+spot_rate) * (q * up_value +(1-q) * down_value)
    else:
        value = (q * up_value +(1-q) * down_value)
    if product.product == "Options":
        if product.type == "American":
            value = max(value, option_value)
    return value

def singlePeriodModelValuation(N, T, product, underlying, up_rate, risk_free_rate, black_scholes):
    up, down, q = getQ(N, T, up, down, risk_free_rate, dividend=0.0, black_scholes=black_scholes)
	
    if product.product == "Options":
        C_u = max((underlying.spot_price_initial * (up) - product.strike_price)*product.type_boolean,0)
        C_d = max((underlying.spot_price_initial * (down) - product.strike_price)*product.type_boolean,0)
        shares = (underlying.spot_price_initial*up - product.strike_price) / float(underlying.spot_price_initial*(up-down))
	
    elif product.product in ("Forwards", "Futures"):
        C_u = underlying.spot_price_initial * (up)
        C_u = underlying.spot_price_initial * (down)
        shares = (underlying.spot_price_initial*up) / float(underlying.spot_price_initial*(up-down))
		
    value = getSingleValue(N, T, product, risk_free_rate, C_u, C_d, q, black_scholes=black_scholes)
    invest_amt = -underlying.spot_price_initial*down*shares / float(1+risk_free_rate)
    return value, shares, invest_amt


def slideWindow(arr):
    new_arr = list()
    for i in range(len(arr)-1):
        new_arr.append([arr[i],arr[i+1]])
    return new_arr

def getMultipleValue(iter, N, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, idx, acc_outcomes, underlying_value=None, underlying_value_list=None, early_exercise_N=0):
    early_exercise = False
    override_value = None
    coupon_payment = None
    spot_rate = None
	
    if iter == 0:
        print("Value at time = " + str(iter) +":\n"+ str(underlying_value))
        if early_exercise_N == 0: early_exercise_N = N
        if product.product == "Options":
            if product.type == "American": print("Option can be early exercised in time:", early_exercise_N)
        acc_outcomes.append(underlying_value)
		
        return list(reversed(acc_outcomes))
    else:

        if underlying_value_list is None:
            #if product.product == "Options":
            #    underlying_value = [max((underlying.spot_price_initial*pow(up,product.N-i)*pow(down,i) - product.strike_price)*product.type_boolean,0) for i in range(0,N+1)]
            #elif product.product in ("Forwards", "Futures"):
            #    underlying_value = [(underlying.spot_price_initial*pow(up,product.N-i)*pow(down,i)) for i in range(0,product.N+1)]
            if product.product == "Stocks":
                underlying_value = [(product.spot_price_initial*pow(up,product.N-i)*pow(down,i)) for i in range(0,product.N+1)]
            elif product.product == "Rates":
                underlying_value = [(product.spot_rate_initial*pow(up,product.N-i)*pow(down,i)) for i in range(0,product.N+1)]
            else: raise ValueError("Please input the underlying lattice!")
            underlying_value_list = underlying_value
        elif underlying_value is None:
            if product.product == "Bonds":
                underlying_value = [product.FV + product.PMT] * (N+1)
            elif product.product in ("Stocks", "Futures"):
                underlying_value = underlying_value_list[product.N]
            elif product.product == "Options":
                underlying_value = [max((u-product.strike_price)*product.type_boolean,0) for u in underlying_value_list[product.N]]

        new_outcomes = list()
        print("Value at time = " + str(iter) +":\n"+ str(underlying_value))
        acc_outcomes.append(underlying_value)

        for j in range(iter):
            if product.product == "Options" and underlying.product == "Stocks": 
                option_value = max((underlying.spot_price_initial*pow(up,iter-j-1)*pow(down,j) - product.strike_price)*product.type_boolean,0)
            elif product.product == "Options" and underlying.product == "Futures":
                option_value = max((underlying_value_list[iter-1][j] - product.strike_price)*product.type_boolean,0)
            else: option_value = 0
            if product.product in ("Stocks"): override_value = underlying_value[idx[j][0]] / float(up) 
            elif product.product in ("Rates"): override_value = underlying_value[idx[j][0]] / float(1+up_rate)
            if product.product == "Bonds": coupon_payment, spot_rate = (product.PMT, underlying_value_list[iter-1][j])
            value = getSingleValue(N, T, product, underlying, up_value=underlying_value[idx[j][0]], down_value=underlying_value[idx[j][1]], q=q, risk_free_rate=risk_free_rate, black_scholes=black_scholes, option_value=option_value, override_value=override_value, coupon_payment=coupon_payment, spot_rate=spot_rate)
            new_outcomes.append(value)
            if value == option_value and value !=0: early_exercise = True or early_exercise
        underlying_value = new_outcomes
        new_idx = slideWindow(list(range(iter)))
        if early_exercise == True: early_exercise_N = iter-1
        
        return getMultipleValue(iter-1, N, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, new_idx, acc_outcomes, underlying_value, underlying_value_list, early_exercise_N=early_exercise_N)

"""
Parameters
black_scholes: Valuation with black scholes equation. Only valid for Options related product
underlying_value_list: Lattice of underlying product
T: Duration for discounting. If discount_period is specified, T becomes the value of discount_period, otherwise it follows the value of T
product: "Rates", "Bonds", "Stocks", "Futures", "Options"
q: Risk neutral probability. If not specified, method: "getQ" is adopted

"""

def multiPeriodModelValuation(T, product, q=None, up_rate=0.0, down_rate=0.0, risk_free_rate=0.0, underlying=None, black_scholes=True, underlying_lattice=None, discount_period=None):
    if discount_period is None: discount_period = product.N
    if underlying is None: underlying = product
    print("Evaluating the " + product.product + ":")
    if q is not None: up, down = (1+up_rate, 1-down_rate)
    elif product.product in ("Stocks", "Futures"):
        up, down, q = getQ(discount_period, T, up_rate, underlying.volatility, risk_free_rate, dividend=0.0, black_scholes=black_scholes)
    else:
        up, down, dummy = getQ(underlying.N, T, up_rate, underlying.volatility, risk_free_rate, dividend=underlying.dividend, black_scholes=black_scholes)
        dummy, dummy, q = getQ(discount_period, T, up_rate, underlying.volatility, risk_free_rate, dividend=product.dividend, black_scholes=black_scholes)

    up_value = 0.0
    down_value = 0.0

    idx = slideWindow(list(range(product.N+1)))
    value = getMultipleValue(product.N, discount_period, T, product, underlying, up, down, up_value, down_value, up_rate, q, risk_free_rate, black_scholes, idx, acc_outcomes=list(), underlying_value=None, underlying_value_list=underlying_lattice, early_exercise_N=0)
    return value


