class Futures:
    def __init__(self, N, spot_price_initial=0.0, volatility=0.0, number_of_contracts=0.0, std_underlying=0.0, std_supplement=0.0, corr=0.0):
        self.product = "Futures"
        self.N = N
        self.spot_price_initial = spot_price_initial
        self.risk_free_rate = 0.0
        self.volatility = volatility
        self.dividend = 0.0
        self.number_of_contracts = number_of_contracts
        self.std_underlying = std_underlying 
        self.std_supplement = std_supplement 
        self.corr = corr
        self.type = None

    def minContracts(self):
        return self.number_of_contracts  * self.corr * self.std_underlying / self.std_supplement

