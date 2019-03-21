from base import CashFlow

class Bonds(CashFlow):
    def __init__(self, N=0, price=0, face_value=0, coupon_rate=0, coupon_period=1):
		# coupon_period: number of coupon periods per year
		
        self.N = N * coupon_period
        self.PV = -price
        self.FV = face_value
        self.PMT = coupon_rate * face_value / coupon_period
        self.mode = 'END'
        self.coupon_period = coupon_period
		
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
        self.YTM = self.getR() * self.coupon_period
        return self.YTM
	
    def macaulayDuration(self):
        cashFlow = [self.PMT]*self.N
        cashFlow[-1] += self.FV
        time = list(range(1,self.N+1))
        return sum([cf*t for cf,t in zip(cashFlow, time)])/float(sum(cashFlow))
	    
    def modifiedDuration(self):
        return self.macaulayDuration() / (1+self.getYTM()/self.coupon_period)
        
	
class AmortizingBonds(Bonds):
    def __init__(self):
         print("")

		 
b = Bonds(10,900,1000,0.05)
result = b.macaulayDuration()
print(result)
print(b.modifiedDuration())