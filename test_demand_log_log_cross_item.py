import unittest
from demand_log_log_cross_item import DemandLogLogCrossItem
from price_discrete import PriceDiscrete

class TestDemandLogLogCrossItem(unittest.TestCase):

    def test_init(self):
        demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='substitute', random_state=0)
        self.assertEqual(demand.model['N_items'], 3)
        self.assertEqual(demand.model['T_periods'], 5)
        self.assertEqual(demand.model['i'], [1, 2, 3]) 
        self.assertEqual(demand.model['j'], [1, 2, 3]) 
        self.assertEqual(demand.model['t'], [1, 2, 3, 4, 5])
        self.assertEqual(demand.model['K_promotion_prices'], {1: 1, 2: 2, 3: 2})
        self.assertEqual(demand.model['k'], {1: [0, 1], 2: [0, 1, 2], 3: [0, 1, 2]})
        self.assertEqual(demand.model['a_seasonality'], {(1, 1): 922.1328742905087, (1, 2): 928.9728088113784, (1, 3): 923.6258693920627, (1, 4): 811.7818483929861, (1, 5): 692.19085364635, (2, 1): 648.7673032722362, (2, 2): 528.3564886587216, (2, 3): 636.3281472900566, (2, 4): 738.832558660675, (2, 5): 906.0843643877465, (3, 1): 739.9885861875287, (3, 2): 696.3923980504148, (3, 3): 918.0393817686888, (3, 4): 668.6980802086342, (3, 5): 824.0859360255986})
        self.assertEqual(demand.model['b_0_price_sensitivity'], {1: 3.84120769920274, 2: 6.7857757947652315, 3: 2.701753902063226})
        self.assertEqual(demand.model['Q_price_ladder'], {(1, 0): 1.0, (1, 1): 0.65, (2, 0): 1.0, (2, 1): 0.825, (2, 2): 0.65, (3, 0): 1.0, (3, 1): 0.825, (3, 2): 0.65})
        self.assertEqual(demand.model['gamma_decision_variable'], {(1, 1, 0): 0, (1, 1, 1): 1, (1, 2, 0): 0, (1, 2, 1): 1, (1, 3, 0): 1, (1, 3, 1): 0, (1, 4, 0): 0, (1, 4, 1): 1, (1, 5, 0): 1, (1, 5, 1): 0, (2, 1, 0): 1, (2, 1, 1): 0, (2, 1, 2): 0, (2, 2, 0): 1, (2, 2, 1): 0, (2, 2, 2): 0, (2, 3, 0): 0, (2, 3, 1): 0, (2, 3, 2): 1, (2, 4, 0): 1, (2, 4, 1): 0, (2, 4, 2): 0, (2, 5, 0): 0, (2, 5, 1): 0, (2, 5, 2): 1, (3, 1, 0): 0, (3, 1, 1): 1, (3, 1, 2): 0, (3, 2, 0): 1, (3, 2, 1): 0, (3, 2, 2): 0, (3, 3, 0): 1, (3, 3, 1): 0, (3, 3, 2): 0, (3, 4, 0): 0, (3, 4, 1): 0, (3, 4, 2): 1, (3, 5, 0): 0, (3, 5, 1): 0, (3, 5, 2): 1})
        self.assertEqual(demand.model['M_num_past_prices'], {1: 0, 2: 1, 3: 1})
        self.assertEqual(demand.model['b_past_price_effects'], {(2, 1): 4.153544339329138, (3, 1): 1.6668038333718365})
        self.assertEqual(demand.model['delta_cross_item_effects'], {(1, 1): 662.643448137331, (1, 2): 297.07419699670123, (1, 3): 51.120319713640455, (2, 1): 558.8984395984697, (2, 2): 78.02507117262483, (2, 3): 239.2177298172088, (3, 1): 344.34533996946476, (3, 2): 101.45161600054197, (3, 3): 97.50166335401799})
        demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='complement', random_state=0)
        self.assertEqual(demand.model['delta_cross_item_effects'], {(1, 1): -309.230591119981, (1, 2): -382.67975329019174, (1, 3): -797.6952782499919, (2, 1): -274.48491812436407, (2, 2): -527.1662093642956, (2, 3): -418.4964456448831, (3, 1): -440.75304523947506, (3, 2): -892.7353030290711, (3, 3): -506.9367146933994})


    # def test_past_price_prod(self):
    #     demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='substitute', random_state=0)
    #     price_discrete = PriceDiscrete(demand.model['t'], demand.model['k'], demand.model['Q_price_ladder'], demand.model['gamma_decision_variable'])
    #     # TODO: Calculate by hand to validate.
    #     prod_answer = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.167081102186562,1.0,0.7256799452675279,0.7256799452675279,1.0,1.0,0.4877118026643013]
    #     prod_test = []
    #     for i in demand.model['i']:
    #         for t in demand.model['t']:
    #             prod_test.append(demand.past_price_prod(i, t, price_discrete))
    #     self.assertEqual(prod_test, prod_answer)
        
    # def test_demand_func(self):
    #     demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='substitute', random_state=0)
    #     price_discrete = PriceDiscrete(demand.model['t'], demand.model['k'], demand.model['Q_price_ladder'], demand.model['gamma_decision_variable'])
    #     # TODO: Calculate by hand to validate.
    #     demand_answer = [4824.276153094345, 4860.060294314934, 923.6258693920627, 4246.958244201317, 692.19085364635, 648.7673032722362, 528.3564886587216, 11836.114294154573, 123.4449582323433, 16853.75406181934, 903.0067834528155, 505.35799730194753, 918.0393817686888, 2141.3721253546946, 1287.0571656519596] 
    #     demand_test = []
    #     for i in demand.model['i']:
    #         for t in demand.model['t']:
    #             demand_test.append(demand.demand_func(i, t, price_discrete))
    #     self.assertEqual(demand_test, demand_answer)

if __name__ == '__main__':
    unittest.main()