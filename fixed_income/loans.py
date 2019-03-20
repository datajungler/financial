from base import CashFlow

class AmortizingLoans(CashFlow):
    def __init__(self, N, r, PV, PMT, mode='END'):
        self.N = N
        self.r = r
        self.PV = PV
        self.FV = 0
        self.PMT = PMT
        self.mode = mode
		
    def setFV(self, mode):
        print("Future Value have to be zero.")
		

    def paySchedule(self):
        self.PMT = round(self.getPMT(),2)
        if self.PMT < 0:
            raise ValueError("Payment should not be negative! Please correct the sign of Present Value.")

        int = [0.0]*(self.N+1)
        principal = [0.0]*(self.N+1)
        end_balance = [0.0]*(self.N+1)
        PMT = [self.PMT]*(self.N+1)
        int[0] = ""
        principal[0] = ""
        end_balance[0] = -self.PV

        for i in range(self.N):
            int[i+1] = round(end_balance[i] * self.r,2)
            principal[i+1] = round(self.PMT - int[i+1],2)
            end_balance[i+1] = round(end_balance[i] - principal[i+1],2)
        
        # TODO: correct the residual in the last payment
        print("Principal Payment, Interest Payment, ")
        result = zip(principal, int, PMT, end_balance)
        return(list(result))

l = AmortizingLoans(60, 0.05, -100000, 0)
print(l.paySchedule())