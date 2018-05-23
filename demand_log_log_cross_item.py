from demand import Demand
from price_discrete import PriceDiscrete
import numpy as np
import json
from math import exp,log
from ast import literal_eval


class DemandLogLogCrossItem(Demand):
    '''
    Class for generating a log-log demand self.model with additive linear cross-item effects.
    '''
    
    def __init__(self, N_items, T_periods, type_of_items, random_state=None, model=None):
        Demand.__init__(self)
        
        if model is None:
            self.model = {}
            np.random.seed(random_state)
            self.model['N_items'] = N_items # Number of items/products.
            self.model['T_periods'] = T_periods # Number of time periods.
            self.model['i'] = [i for i in range(1, self.model['N_items']+1)] # Item index list (1-indexed).
            self.model['j'] = [i for i in range(1, self.model['N_items']+1)] # Cross-item index list (1-indexed).
            self.model['t'] = [i for i in range(1, self.model['T_periods']+1)] # Time index (1-indexed).
            self.model['K_promotion_prices'] = {i: int(np.random.randint(low=1, high=3, size=1)[0]) for i in self.model['i']} # Dict mapping items to randomly generated number of promotion prices (1 or 2).
            self.model['k'] = {i: [j for j in range(0, self.model['K_promotion_prices'][i]+1)] for i in self.model['i']} # Dict mapping items to price index lists (0-indexed). 
            self.model['a_seasonality'] = {(i,t): float(np.random.uniform(low=500.0, high=1000.0, size=1)[0]) for i in self.model['i'] for t in self.model['t']} # Dict mapping item/time combinations to randomly generated seasonality coefficients.
            self.model['b_0_price_sensitivity'] = {i: float(np.random.uniform(low=2.0, high=7.0, size=1)[0]) for i in self.model['i']} # Dict mapping items to randomly generated price sensitivities (elasticities).
            self.model['Q_price_ladder'] = {(i,k): float(list(np.linspace(1.0, 0.65, num=self.model['K_promotion_prices'][i]+1))[k]) for i in self.model['i'] for k in self.model['k'][i]}  # Price ladder dict mapping item/price index combinations to prices between 1 (base/regular price normalized) and 0.65.
            self.model['gamma_decision_variable'] = {(i,t,k): 0 for i in self.model['i'] for t in self.model['t'] for k in self.model['k'][i]} # Dict mapping item/time/price index combinations to randomly generated integer (binary) decision variables that act to select exactly one price from the price ladder for each item at each time.
            for i in self.model['i']:
                for t in self.model['t']:
                    selection = np.array([1] * 1 + [0] * self.model['K_promotion_prices'][i])
                    np.random.shuffle(selection)
                    for k in self.model['k'][i]:
                        self.model['gamma_decision_variable'][i,t,k] = int(selection[k])
            self.model['M_num_past_prices'] = {i: int(np.random.choice(np.asarray([0,1,2,3]))) for i in self.model['i']} # Dict mapping items to randomly generated number of past prices to consider (memory).
            self.model['b_past_price_effects'] = {(i,k): float(np.random.uniform(low=0.0, high=self.model['b_0_price_sensitivity'][i], size=1)[0]) for i in self.model['i'] for k in range(1, self.model['M_num_past_prices'][i]+1)} # Dict mapping item/past price combinations to randomly generated past price effects.
            # Dict mapping cross-item/item combinations to substitute or complement cross-item effects.
            if type_of_items == 'substitute':
                self.model['delta_cross_item_effects'] = {(j,i): float(np.random.uniform(low=0.0, high=np.random.uniform(low=500.0, high=1000.0, size=1)[0], size=1)[0]) for j in self.model['j'] for i in self.model['i']}
            elif type_of_items == 'complement':
                self.model['delta_cross_item_effects'] = {(j,i): float(np.random.uniform(low=-np.random.uniform(low=500.0, high=1000.0, size=1)[0], high=0.0, size=1)[0]) for j in self.model['j'] for i in self.model['i']}
        else:
            self.model = model
        
    def export_model(self):
        '''
        Export a model to properly formatted json.
        '''
        model = dict(self.model)
        model['K_promotion_prices'] = {str(i): self.model['K_promotion_prices'][i] for i in self.model['i']} # Dict mapping items to randomly generated number of promotion prices (1 or 2).
        model['k'] = {str(i): self.model['k'][i] for i in self.model['i']} # Dict mapping items to price index lists (0-indexed). 
        model['a_seasonality'] = {str((i,t)): self.model['a_seasonality'][(i,t)] for i in self.model['i'] for t in self.model['t']} # Dict mapping item/time combinations to randomly generated seasonality coefficients.
        model['b_0_price_sensitivity'] = {str(i): self.model['b_0_price_sensitivity'][i] for i in self.model['i']} # Dict mapping items to randomly generated price sensitivities (elasticities).
        model['Q_price_ladder'] = {str((i,k)): self.model['Q_price_ladder'][(i,k)] for i in self.model['i'] for k in self.model['k'][i]}  # Price ladder dict mapping item/price index combinations to prices between 1 (base/regular price normalized) and 0.65.
        model['gamma_decision_variable'] = {str((i,t,k)): self.model['gamma_decision_variable'][(i,t,k)] for i in self.model['i'] for t in self.model['t'] for k in self.model['k'][i]} # Dict mapping item/time/price index combinations to randomly generated integer (binary) decision variables that act to select exactly one price from the price ladder for each item at each time.
        model['M_num_past_prices'] = {str(i): self.model['M_num_past_prices'][i] for i in self.model['i']} # Dict mapping items to randomly generated number of past prices to consider (memory).
        model['b_past_price_effects'] = {str((i,k)): self.model['b_past_price_effects'][(i,k)] for i in self.model['i'] for k in range(1, self.model['M_num_past_prices'][i]+1)} # Dict mapping item/past price combinations to randomly generated past price effects.
        model['delta_cross_item_effects'] = {str((j,i)): self.model['delta_cross_item_effects'][(j,i)] for j in self.model['j'] for i in self.model['i']}
        return model
        
    def load_model(self, model):
        '''
        Load a model from a json string.
        '''
        model = dict(json.loads(model))
        self.model['N_items'] = model['N_items'] # Number of items/products.
        self.model['T_periods'] = model['T_periods'] # Number of time periods.
        self.model['i'] = model['i'] # Item index list (1-indexed).
        self.model['j'] = model['j'] # Cross-item index list (1-indexed).
        self.model['t'] = model['t'] # Time index (1-indexed).
        self.model['K_promotion_prices'] = {i: model['K_promotion_prices'][str(i)] for i in model['i']} # Dict mapping items to randomly generated number of promotion prices (1 or 2).
        self.model['k'] = {i: model['k'][str(i)] for i in model['i']} # Dict mapping items to price index lists (0-indexed). 
        self.model['a_seasonality'] = {(i,t): model['a_seasonality'][str((i,t))] for i in model['i'] for t in model['t']} # Dict mapping item/time combinations to randomly generated seasonality coefficients.
        self.model['b_0_price_sensitivity'] = {i: model['b_0_price_sensitivity'][str(i)] for i in model['i']} # Dict mapping items to randomly generated price sensitivities (elasticities).
        self.model['Q_price_ladder'] = {(i,k): model['Q_price_ladder'][str((i,k))] for i in model['i'] for k in model['k'][str(i)]}  # Price ladder dict mapping item/price index combinations to prices between 1 (base/regular price normalized) and 0.65.
        self.model['gamma_decision_variable'] = {(i,t,k): model['gamma_decision_variable'][str((i,t,k))] for i in model['i'] for t in model['t'] for k in model['k'][str(i)]} # Dict mapping item/time/price index combinations to randomly generated integer (binary) decision variables that act to select exactly one price from the price ladder for each item at each time.
        self.model['M_num_past_prices'] = {i: model['M_num_past_prices'][str(i)] for i in model['i']} # Dict mapping items to randomly generated number of past prices to consider (memory).
        self.model['b_past_price_effects'] = {(i,k): model['b_past_price_effects'][str((i,k))] for i in model['i'] for k in range(1, model['M_num_past_prices'][str(i)]+1)} # Dict mapping item/past price combinations to randomly generated past price effects.
        self.model['delta_cross_item_effects'] = {(j,i): model['delta_cross_item_effects'][str((j,i))] for j in model['j'] for i in model['i']}
        return self.model
    
    def past_price_prod(self, i, t, price_model):
        '''
        Utility function for calculating past price product sum part of demand function.
        '''
        return np.prod(np.asarray([np.power(price_model.price_func(i, t-k), self.model['b_past_price_effects'][i,k]) for k in range(1, self.model['M_num_past_prices'][i]+1)]))
    
    
    def cross_item_sum(self, i, t, price_model):
        '''
        Utility function for calculating additive linear cross-item effects part of demand function.
        '''
        return sum(self.model['delta_cross_item_effects'][j,i] * price_model.price_func(j,t) for j in self.model['j'])
        
        
    def demand_func(self, i, t, price_model):
        '''
        Define a function representing the demand for item i at time t.
        '''
        return self.model['a_seasonality'][i,t] * exp(-self.model['b_0_price_sensitivity'][i] * log(price_model.price_func(i,t))) * self.past_price_prod(i, t, price_model) + self.cross_item_sum(i, t, price_model)
        
        
if __name__ == '__main__':
    log_log_demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='complement', random_state=0)    
        
        
        

        
        
    # def demand_expr(self, self.model, i, t):
    #     '''
    #     Define and return a Pyomo expression representing the demand for item i at time t.
    #     '''
    #     return exp(13.702502883987158 - 3.954257092854971 * self.price_expr(self.model, i, t))