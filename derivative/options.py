from pricing import singlePeriodModelValuation, multiPeriodModelValuation
import matplotlib.pyplot as plt

class Options:
    def __init__(self, N, call_put, spot_price_initial, strike_price, dividend, volatility, type, buy=True):
        self.product = "Options"
        self.N = N
        self.spot_price_initial = spot_price_initial
        self.strike_price = strike_price
        self.call_put = call_put
        self.dividend= dividend
        self.volatility = volatility
        self.type = type
		self.buy = buy

        if self.call_put not in ('call', 'put'): raise ValueError("Please input the suitable options type.")
        if self.call_put == 'put': self.type_boolean = -1
        else: self.type_boolean = 1
		
        self.value = max(strike_price - spot_price_initial, 0) * self.type_boolean
        if self.type not in ('American', 'European'):
            raise ValueError("Please input the suitable options type: American / European.")

    def payOff(self, price_list, plot_graph=False):
        if self.strike_price not in price_list: raise ValueError("Please include the strike price in the list of underlying price!")
        payOff_list = [max((price - self.strike_price)*self.type_boolean, 0) for price in price_list]
        if plot_graph:
            plt.plot(price_list, payOff_list)
            plt.show()
        return payOff_list