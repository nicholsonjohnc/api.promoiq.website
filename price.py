class Price(object):
    '''
    Base class all future price models should derive from.
    '''
    
    def __init__(self):
        pass
    
    def price_func(self, i, t):
        '''
        Define a function that returns the price of item i at time t.
        '''
        pass