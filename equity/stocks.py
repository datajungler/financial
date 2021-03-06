from .base import CAPM

class Stocks:
    def __init__(self, N=0.0, stock_id='', stock_name='', spot_price_initial=0.0, dividend=0.0, growth_rate=0.0, type='common', required_rate_of_return=0.0, volatility=0.0, market_data=None):
        self.product = "Stocks"
        self.N = N
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.spot_price_initial = spot_price_initial
        self.dividend = dividend
        self.growth_rate = growth_rate
        self.type = type
        self.market_data = market_data
        self.required_rate_of_return = required_rate_of_return
        self.volatility = volatility
    
    def cost_of_equity(self):
        if self.market_data is not None:
            print("As market information is available, cost of equity is computed under CAPM.")
            cost_of_equity = CAPM(self.market_data['risk_free_rate'], self.market_data['market_return'], self.market_data['stock_beta'])
        else:
            print("As market information is unknown, cost of equity is computed under stock dividend.")
            cost_of_equity = self.dividend*(1+self.growth_rate) / float(self.spot_price_initial) + self.growth_rate
			
		
    def value(self):
        if self.type == 'preferred':
            value = spot_price_initial
        elif self.type == 'common':
            if self.market_data is not None:
                print("As market information is available, cost of equity is computed under CAPM.")
                cost_of_equity = CAPM(self.market_data['risk_free_rate'], self.market_data['market_return'], self.market_data['stock_beta'])

            elif self.required_rate_of_return != 0.0:
                cost_of_equity = self.required_rate_of_return

            else:
                raise ValueError("Please input required rate of return.")

					
            if isinstance(self.dividend, list) == False: 
                print("Valuation with Constant Growth Model.")
                value = self.dividend*(1+self.growth_rate) / float(cost_of_equity-self.growth_rate)
			
            else:
                print("A time series of dividend is received. Valuation with Multiple Dividend Growth Model.")
                discount = [1/pow(float(1+cost_of_equity),i) for i in range(len(self.dividend))]
                value = sum(d[0] * d[1] for d in zip(self.dividend, discount)) + self.dividend[-1]*(1+self.growth_rate)/float(cost_of_equity-self.growth_rate)/pow(float(1+cost_of_equity),len(self.dividend))
			
        return value

