import matplotlib.pyplot as plt

class Options:
    def __init__(self, N, call_put, spot_price_initial=0.0, strike_price=0.0, dividend=0.0, volatility=0.0, type="European", buy=True):
        self.product = "Options"
        self.N = N
        self.spot_price_initial = spot_price_initial
        self.strike_price = strike_price
        self.call_put = call_put
        self.dividend = dividend
        self.volatility = volatility
        self.type = type
        self.buy = buy

        if self.call_put not in ('call', 'put'): raise ValueError("Please input the suitable options type.")
        if self.call_put == 'put': self.type_boolean = -1
        else: self.type_boolean = 1
		
        if self.type not in ('American', 'European'):
            raise ValueError("Please input the suitable options type: American / European.")

    def payOff(self, price_list, plot_graph=False):
        if self.strike_price not in price_list: raise ValueError("Please include the strike price in the list of underlying price!")
        payOff_list = [max((price - self.strike_price)*self.type_boolean, 0) for price in price_list]
        if plot_graph:
            plt.plot(price_list, payOff_list)
            plt.show()
        return payOff_list


class CapFloors():
    def __init__(self, N, cap_floor, fixed_rate=0.0, buy=True):
        self.product = "CapFloor"
        self.N = N
        self.fixed_rate = fixed_rate
        self.cap_floor = cap_floor
        self.type ="European"
        self.buy = buy

        if self.cap_floor not in ('cap', 'floor'): raise ValueError("Please input the suitable options type.")
        if self.cap_floor == 'floor': self.type_boolean = -1
        else: self.type_boolean = 1
		
        if self.type not in ('American', 'European'):
            raise ValueError("Please input the suitable options type: American / European.")

class Swaptions():
    def __init__(self, N, strike_rate, buy=True):
        self.product = "Swaptions"
        self.N = N
        self.strike_rate = strike_rate
        self.type = "" # TODO
        self.buy = True
		
		
		
		
		
		

		
		