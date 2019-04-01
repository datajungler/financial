from .base import CashFlow

class Bonds(CashFlow):
    def __init__(self, N=0, price=0, face_value=0, coupon_rate=0, coupon_compound_period=1, price_lower=0.0, price_upper=0.0, delta_YTM=0.0):
		# coupon_compound_period: number of coupon periods per year
        self.product = "Bonds"
        self.N = N * coupon_compound_period
        self.price = price
        self.PV = -price
        self.FV = face_value
        self.PMT = coupon_rate * face_value / coupon_compound_period
        self.mode = 'END'
        self.coupon_compound_period = coupon_compound_period
        self.price_lower = price_lower
        self.price_upper = price_upper
        self.delta_YTM = delta_YTM
        self.convexity = 0.0
		
        if price - face_value > 0:
            self.type = 'premium'
        elif price - face_value < 0:
            self.type = 'discount'
        else:
            self.type = 'par'
			
        # TODO: credit rating

    def setMode(self, mode):
        print("Failed. Annuity Immediate should be computed under 'END' mode.")
		
    def getYTM(self):
        self.YTM = self.getR() * self.coupon_compound_period
        return self.YTM
	
    def macaulayDuration(self):
        cashFlow = [self.PMT]*self.N
        cashFlow[-1] += self.FV
        time = list(range(1,self.N+1))
        return sum([cf*t for cf,t in zip(cashFlow, time)])/float(sum(cashFlow))
	    
    def modifiedDuration(self):
        return self.macaulayDuration() / (1+self.getYTM()/self.coupon_compound_period)
    
    def effectiveDuration(self):
        return (self.price_upper - self.price_lower) / float(2*self.price*pow(self.delta_YTM, 2))
	
    def getConvexity(self):
        self.convexity = (self.price_upper - self.price_lower + 2*self.price) / float(self.price*pow(self.delta_YTM, 2))
        return self.convexity

    def pricePercentChange(self):
	    return -self.modifiedDuration() * self.delta_YTM + 0.5 * self.getConvexity() * pow(self.delta_YTM,2)
	
	
class AmortizingBonds(Bonds):
    def __init__(self):
         print("")


		 


