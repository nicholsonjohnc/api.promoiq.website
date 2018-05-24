import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['font.size'] = 16
mpl.rcParams['legend.fontsize'] = 'medium'
mpl.rcParams['figure.titlesize'] = 'medium'
mpl.rcParams['xtick.major.width'] = 1
mpl.rcParams['ytick.major.width'] = 1
mpl.rcParams['axes.linewidth'] = 1
mpl.rcParams['axes.titlesize'] = 'large'
import matplotlib.pyplot as plt

from io import StringIO

class PlotPromotionPlan(object):
    
    def __init__(self, model, price):
        self.model = model
        self.price = price
        
    def plot(self):
        
        prices = []
        for i in self.model['i']:
            prices.append([])
            for t in self.model['t']:
                prices[i-1].append(self.price.price_func(i,t))
        
        fig, ax = plt.subplots(1, 1, figsize=(12,6))
        
        for i in self.model['i']:
            ax.plot(self.model['t'], prices[i-1], label='Product ' + str(i))
            
        ax.set_title('Promotion Plan')
        ax.set_xlabel('Week')
        ax.set_ylabel('Price Index')
        ax.legend(loc=1)
        plt.tight_layout()
        
        # Create a file buffer.
        fig_file = StringIO()
        # Save svg in buffer.
        plt.savefig(fig_file, format='svg')
        # Retrieve the svg.
        fig_file_svg = '<svg' + fig_file.getvalue().split('<svg')[1]
        # Discard buffer.
        fig_file.close()
        
        return fig_file_svg