from pricing import singlePeriodModelValuation, multiPeriodModelValuation

class Options:
    def __init__(self, option_type, spot_price_initial, strike_price, dividend):
        self.product = "Options"
        self.spot_price_initial = spot_price_initial
        self.strike_price = strike_price
        self.option_type = option_type
        self.dividend= dividend
        if self.option_type == 'call':
            self.value = max(spot_price_initial - strike_price, 0)
        elif self.option_type == 'put':
            self.value = max(strike_price - spot_price_initial, 0)
        else:
            raise ValueError("Please input the suitable options type.")
		


opt = Options(option_type='call', spot_price_initial=100, strike_price=100, dividend=0.0)
print(singlePeriodModelValuation(product=opt, up_rate=0.06, risk_free_rate=0.02))
result = multiPeriodModelValuation(N=3, product=opt, up_rate=0.07, risk_free_rate=0.01)
print(result)