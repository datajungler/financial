from math import exp, log

def discountRate(spot_rate_list, continuous=False, compound_period=1):
    spot_rate_list_compound = list()
    for sr in spot_rate_list:
        for p in range(compound_period):
            spot_rate_list_compound.append(sr/float(compound_period))
    
    N = len(spot_rate_list_compound)
    d_list = list()
    for i in range(N):
        if continuous == False:
            d_list.append(1/float(pow(1+spot_rate_list_compound[i],i+1)))
        elif continuous == True:
            d_list.appennd(1/exp((i+1)*spot_rate_list_compound[i]))
        else:
            raise ValueError("Please input boolean value!")
        
    return d_list


def EAR(r, compound_period=1, continuous=False):
# r: periodic rate
# compound_period: number of compounding period per year

    if continuous == True:
        print("Compound Period assume to be infinity.")
        ear = exp(r) - 1
    else:
        ear = pow(1+r/m,m) - 1
    return ear


def forwardRate(spot_rate_list, start_N, end_N):
    spot_end_N = pow(1+spot_rate_list[end_N-1], end_N)
    spot_start_N = pow(1+spot_rate_list[start_N-1], start_N)
    print(spot_end_N)
    print(spot_start_N)
    return spot_end_N / float(spot_start_N) - 1
	
