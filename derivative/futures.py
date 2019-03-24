class Futures:
    def __init__(self, spot_price_inital, risk_free_rate, number_of_contracts, std_underlying, std_supplement, corr):
        self.product = "Futures"
        self.spot_price_inital = spot_price_inital
        self.risk_free_rate = risk_free_rate
        self.number_of_contracts = number_of_contracts
        self.std_underlying = std_underlying 
        self.std_supplement = std_supplement 
        self.corr = corr

    def minContracts(self):
        return self.number_of_contracts  * self.corr * self.std_underlying / self.std_supplement

f = Futures(10, 0.25, 0.2, 0.7)
print(f.minVarHedge())