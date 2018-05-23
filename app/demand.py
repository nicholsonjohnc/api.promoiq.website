class Demand(object):
    '''
    Base class all future demand models should derive from.
    '''
    
    def __init__(self):
        pass
    
    def demand_func(self, i, t):
        '''
        Define a function that returns the demand for item i at time t.
        '''
        pass