import sys
import matplotlib.pyplot as plt
import numpy as np
import bruges
import collections
from matplotlib import colors
from PIL import Image

def main():

    script = sys.argv[0]
    image = sys.argv[1]
    frequency = sys.argv[2]
    file_name = sys.argv[3]
        
    def sketchthetic(image, frequency, file_name):
            
        ### Load image fill and plot ###
        
        fig, ax = plt.subplots(figsize = (8, 6), nrows = 2)
        channel = np.asarray(Image.open(image))
        ax[0].imshow(channel, aspect= 'auto')
        ax[0].axes.xaxis.set_ticklabels([])
        ax[0].axes.yaxis.set_ticklabels([])
        ax[0].axes.xaxis.set_ticks([])
        ax[0].axes.yaxis.set_ticks([])
            
        ### Resize image ###

        x = channel.shape[0] 
        y = channel.shape[1] * channel.shape[2] 
        channel.resize((x,y))
        
        ### Find most frequent image array values and sort ###
        
        flattened = channel.flatten()
        counted = collections.Counter(flattened)
        counted = {k: v for k, v in sorted(counted.items(), key = lambda item: item[1], reverse = True)}
        keys = np.array(list(counted.keys()))
        keys = sorted(keys[0:5])
        
        ### Collapse image array by most frequent values and assign single values ###

        channel = np.where((channel > 0) & (channel <= (keys[1])), 1, channel)
        channel = np.where((channel > keys[1]) & (channel <= keys[2]), 2, channel)
        channel = np.where((channel > keys[2]) & (channel <= keys[3]), 3, channel)
        channel = np.where((channel > keys[3]) & (channel <= keys[4]), 4, channel)
        channel = np.where((channel > keys[4]), 5, channel)
        
        ### Assign sonic and density values [Vp, rho] ###
        
    #     zero = [2700, 2750]
    #     one = [3100, 3150] 
    #     two = [2200, 2250]
    #     three = [2800, 3000]
    #     four = [2100, 2150]
        
        zero = [2200, 2250]
        one = [2300, 2350] 
        two = [2400, 2450]
        three = [2500, 2550]
        four = [2600, 2650]
        
        ### Make array of "rocks" and index into image array ###

        rocks = np.array([zero, one, two, three, four])
        earth = rocks[channel]
        
        ### Calculate acoustic impedance ###
        
        imp = np.apply_along_axis(np.product, -1, earth)
        rc = np.diff(imp, axis=0)
        
        ### Create wavelet and convolve with image ###

        w = bruges.filters.ricker(duration = 0.1, dt = 0.001, f = frequency)
        synth = np.apply_along_axis(lambda t: np.convolve(t, w, mode = 'same'), axis = 0, arr = rc)
        
        ### Plot ###

        ax[1].imshow(synth, cmap = "RdBu", aspect = 'auto', vmin = -1e6, vmax = 1e6)
        ax[1].axes.xaxis.set_ticklabels([])
        ax[1].axes.yaxis.set_ticklabels([])
        ax[1].axes.xaxis.set_ticks([])
        ax[1].axes.yaxis.set_ticks([])

        plt.tight_layout()
        plt.show()
        plt.savefig('figures/{}.jpg'.format(file_name), bbox_inches = 'tight', dpi = 96)

main()