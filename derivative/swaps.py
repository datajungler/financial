import sys
sys.path.insert(0, "..")
from interest_rate.base import discountRate

class Swap:
    def __init__(self, spot_rate_list, value=0, commpound_period=1):
        self.spot_rate_list = spot_rate_list
        self.value = value
        self.commpound_period = commpound_period
        self.fixed_rate = 0.0

    def getRate(self):
        dr_list = discountRate(self.spot_rate_list, False, self.commpound_period)
        self.fixed_rate = (1 - dr_list[len(dr_list)-1])/sum(dr_list)
        return self.fixed_rate
