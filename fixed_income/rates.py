class Rates():
    def __init__(self, N, spot_rate_initial):
		# coupon_compound_period: number of coupon periods per year
        self.product = "Rates"
        self.N = N
        self.spot_rate_initial = spot_rate_initial