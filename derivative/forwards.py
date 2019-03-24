from pricing import singlePeriodModelValuation, multiPeriodModelValuation

class Forwards:
    def __init__(self, spot_price_initial):
        self.product = "Forwards"
        self.spot_price_initial = spot_price_initial


f = Forwards(spot_price_initial=100)
print(multiPeriodModelValuation(N=3, product=f, up_rate=0.06, risk_free_rate=0.02))
