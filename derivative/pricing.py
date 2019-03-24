# TODO: add underlying stock dividend component into valuation model
def singlePeriodModelValuation(product, up_rate, risk_free_rate):
    up = 1 + up_rate
    down = 1/float(up)
    q = (1+risk_free_rate-down)/float(up-down)
	
    if product.product == "Options":
        if product.option_type not in ('call', 'put'): raise ValueError("Please input the suitable options type.")
        if product.option_type == 'put': type_boolean = -1
        else: type_boolean = 1
        C_u = max((product.spot_price_initial * (up) - product.strike_price)*type_boolean,0)
        C_d = max((product.spot_price_initial * (down) - product.strike_price)*type_boolean,0)
        shares = (product.spot_price_initial*up - product.strike_price) / float(product.spot_price_initial*(up-down))
	
    elif product.product in ("Forwards", "Futures"):
        C_u = product.spot_price_initial * (up)
        C_u = product.spot_price_initial * (down)
        shares = (product.spot_price_initial*up) / float(product.spot_price_initial*(up-down))
		
    value = 1/float(1+risk_free_rate) * (q * C_u +(1-q) * C_d)
    invest_amt = -product.spot_price_initial*down*shares / float(1+risk_free_rate)
    return value, shares, invest_amt

def singlePeriodModelValuationByValue(up_value, down_value, up_rate, risk_free_rate):
    up = 1 + up_rate
    down = 1/float(up)
    q = (1+risk_free_rate-down)/float(up-down)
    value = 1/float(1+risk_free_rate) * (q * up_value +(1-q) * down_value)
    return value

def slideWindow(arr):
    new_arr = list()
    for i in range(len(arr)-1):
        new_arr.append([arr[i],arr[i+1]])
    return new_arr

def multiPeriodModelValuationByValue(N, product, up_value, down_value, up_rate, risk_free_rate, outcomes, idx):
    if N == 0:
        print("Value at time = " + str(N) +":\n"+ str(outcomes))
        return outcomes[0]
    else:
        new_outcomes = list()

        for j in range(len(idx)):
            new_outcomes.append(singlePeriodModelValuationByValue(up_value=outcomes[idx[j][0]], down_value=outcomes[idx[j][1]], up_rate=up_rate, risk_free_rate=risk_free_rate))

        new_idx = slideWindow(list(range(N)))
        print("Value at time = " + str(N) +":\n"+ str(outcomes))
        return multiPeriodModelValuationByValue(N-1, product, up_value, down_value, up_rate, risk_free_rate, new_outcomes, new_idx)

def multiPeriodModelValuation(N, product, up_rate, risk_free_rate):
    up = 1 + up_rate
    down = 1/float(up)
    q = (1+risk_free_rate-down)/float(up-down)
	
    if product.product == "Options":
        if product.option_type not in ('call', 'put'): raise ValueError("Please input the suitable options type.")
        if product.option_type == 'put': type_boolean = -1
        else: type_boolean = 1
        up_value = max((product.spot_price_initial * (up) - product.strike_price)*type_boolean,0)
        down_value = max((product.spot_price_initial * (down) - product.strike_price)*type_boolean,0)
        outcomes = [max((product.spot_price_initial*pow(up,N-i)*pow(down,i) - product.strike_price)*type_boolean,0) for i in range(0,N+1)]
	
    elif product.product in ("Forwards", "Futures"):
        up_value = product.spot_price_initial * (up)
        down_value = product.spot_price_initial * (down)
        outcomes = [(product.spot_price_initial*pow(up,N-i)*pow(down,i)) for i in range(0,N+1)]
		
    idx = slideWindow(list(range(N+1)))
    value = multiPeriodModelValuationByValue(N, product, up_value, down_value, up_rate, risk_free_rate, outcomes, idx)
    return value



