from price import Price

class PriceDiscrete(Price):
    '''
    Class representing a discrete price model.
    '''
    
    def __init__(self, t_set, k_set, Q_price_ladder, gamma_decision_variable):
        Price.__init__(self)
        self.t_set = t_set
        self.k_set = k_set
        self.Q_price_ladder = Q_price_ladder
        self.gamma_decision_variable = gamma_decision_variable
    
    
    def price_func(self, i, t):
        '''
        Define a function that returns the price of item i at time t.
        '''
        # If requesting a price that occurs before the first period then return the first period price. 
        if t < self.t_set[0]:
            return sum(self.Q_price_ladder[i,k] * self.gamma_decision_variable[i,self.t_set[0],k] for k in self.k_set[i])
        else:
            return sum(self.Q_price_ladder[i,k] * self.gamma_decision_variable[i,t,k] for k in self.k_set[i])