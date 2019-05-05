import sys
sys.path.insert(0, "..")
from interest_rate.base import discountRate

class Swaps:
    def __init__(self, N, fixed_rate, value=0, commpound_period=1):
        self.N = N
        self.product = "Swaps"
        self.value = value
        self.fixed_rate = fixed_rate
        self.commpound_period = commpound_period

    def getRate(self, spot_rate_list):
        dr_list = discountRate(spot_rate_list, False, self.commpound_period)
        self.fixed_rate = (1 - dr_list[len(dr_list)-1])/sum(dr_list)
        return self.fixed_rate

		