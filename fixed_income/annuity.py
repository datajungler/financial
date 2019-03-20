from base import CashFlow, EAR


class AnnuityImmediate(CashFlow):
    def __init__(self, N=0, r=0, PV=0, PMT=0):
        self.N = N
        self.r = r
        self.PV = PV
        self.FV = 0
        self.PMT = PMT
        self.mode = 'END'
		
    def setFV(self, mode):
        print("Future Value have to be zero.")
		
    def setMode(self, mode):
        print("Failed. Annuity Immediate should be computed under 'END' mode.")



class AnnuityDue(CashFlow):
    def __init__(self, N=0, r=0, PV=0, PMT=0):
        self.N = N
        self.r = r
        self.PV = PV
        self.FV = 0
        self.PMT = PMT
        self.mode = 'BGN'
		
    def setFV(self, mode):
        print("Future Value have to be zero.")
		
    def setMode(self, mode):
        print("Failed. Annuity Due have should be computed under 'BGN' mode.")


		
class Perpetuity(AnnuityImmediate):
    def __init__(self, r, PV=0, PMT=0):
        self.N = 9999
        self.r = r
        self.PV = PV
        self.FV = 0
        self.PMT = PMT
        self.mode = 'END'



ai = Perpetuity(0.05, 0, 500)
result = ai.getPV()
print(result)

