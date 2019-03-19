from math import exp

class CashFlow:
    def __init__(self, N=0, r=0, PV=0, FV=0, PMT=0, mode='END'):
        self.N = N
        self.r = r
        self.PV = PV
        self.FV = FV
        self.PMT = PMT
		
    def setN(self, N):
        self.N = N

    def setPV(self, PV):
        self.PV = PV

    def setFV(self, FV):
        self.FV = FV

    def setPMT(self, PMT):
        self.PMT = PMT

    def setMode(self, mode):
        if mode not in ('END', 'BGN'):
            print("Please specify the mode ('END' / 'BGN')")
        else:
            self.mode = mode
		
    def getFV(self):
        FV_0 = -self.PMT/float(self.r) * (pow(1+self.r,self.N) - 1)
        FV_1 = -self.PV * pow(1+self.r,self.N)
		
        if self.mode == 'END':
            self.FV = FV_0 + FV_1
        elif self.mode == 'BGN':
            self.FV = FV_0 * (1+self.r) + FV_1
		
        return self.FV
		
    def getPV(self):    
        v = 1/float(1+self.r)
        PV_0 = -self.PMT/float(self.r) * (1-pow(v,self.N))
        PV_1 = -self.FV / float(pow(1+self.r,self.N))

        if self.mode == 'END':
            self.PV = PV_0 + PV_1
        elif self.mode == 'BGN':
            self.PV = PV_0 * (1+self.r) + PV_1

        return self.PV

    def getPMT(self):
        v = 1/float(1+self.r)
        d = 1 - v
        PMT = - (self.PV + self.FV/float(pow(1+self.r,self.N))) 

        if mode == 'END':
            self.PMT = self.PMT * float(self.r) / (1-pow(v,self.N)) 
        elif mode == 'BGN':
            self.PMT = self.PMT * float(d) / (1-pow(v,self.N)) 

        return self.PMT


def EAR(r, m=1):
# r: periodic rate
# m: number of compounding period per year

    if m == 'continous':
        ear = exp(r) - 1
    else:
        ear = pow(1+r/m,m) - 1
    return ear


if __name__ == '__main__':
    main()