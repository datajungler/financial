class Options:
    def __init__(self, spot_price, strike_price):
        self.spot_price = spot_price
        self.strike_price = strike_price

		
class CallOptions(Options):
    def __init__(self, spot_price, strike_price):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.value = max(spot_price - strike_price, 0)
		
    def get(self):
        print()
		
class PutOptions(Options):
    def __init__(self, spot_price, strike_price):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.value = max(strike_price - spot_price, 0)
		
    def get(self):
        print()

def SinglePeriodModelValuation(spot_price_initial, strike_price, up_rate, risk_free_rate):
    up = 1 + up_rate
    down = 1/float(up)
    q = (1+risk_free_rate-down)/float(up-down)
    C_u = spot_price_initial * up - strike_price
    value = q * C_u / float(1+risk_free_rate)
    shares = (spot_price_initial*up - strike_price) / float(spot_price_initial*(up-down))
    invest_amt = -spot_price_initial*down*shares / float(1+risk_free_rate)
    return value, shares, invest_amt

