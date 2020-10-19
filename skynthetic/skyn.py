import matplotlib.pyplot as plt
import numpy as np
import bruges
import collections
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image

def go(sketch, frequency, amp_min = -1e6, amp_max = 1e6, output_name = None):
    
    """Make synthetic seismic section from image

    Parameters:
    
    sketch: Path to sketch. Include extension (e.g. .png, .jpeg, .tiff). Try to resize image to 96 dpi for better results.
    frequency: Centre frequency of the wavelet [Hz]. Note that this is the relative frequency because the images are not scaled.
    amp_min: Minimum amplitude for colorbar. Default is -1e6.
    amp_max: Maximum amplitude for colorbar. Default is 1e6.
    output_name: Saves output image in figures folder (default is not to save the image).

    Returns:
    
    jpg of synthetic seismic section

    """

    ### Load image fill and plot ###

    fig, ax = plt.subplots(figsize = (10, 8), nrows = 2)
    sketch = np.asarray(Image.open(sketch))
    print("Sketch loaded...")
    ax[0].imshow(sketch, aspect= 'auto')
    ax[0].axes.xaxis.set_ticklabels([])
    ax[0].axes.yaxis.set_ticklabels([])
    ax[0].axes.xaxis.set_ticks([])
    ax[0].axes.yaxis.set_ticks([])

    ### Resize image ###

    x = sketch.shape[0] 
    y = sketch.shape[1] * sketch.shape[2] 
    sketch.resize((x,y))

    ### Find most frequent image array values and sort ###

    flattened = sketch.flatten()
    counted = collections.Counter(flattened)
    counted = {k: v for k, v in sorted(counted.items(), key = lambda item: item[1], reverse = True)}
    keys = np.array(list(counted.keys()))
    keys = sorted(keys[0:5])

    ### Collapse image array by most frequent values and assign single values ###

    sketch = np.where((sketch > 0) & (sketch <= (keys[1])), 1, sketch)
    sketch = np.where((sketch > keys[1]) & (sketch <= keys[2]), 2, sketch)
    sketch = np.where((sketch > keys[2]) & (sketch <= keys[3]), 3, sketch)
    sketch = np.where((sketch > keys[3]) & (sketch <= keys[4]), 4, sketch)
    sketch = np.where((sketch > keys[4]), 5, sketch)

    ### Assign sonic and density values [Vp, rho] ###

    zero = [2200, 2250]
    one = [2300, 2350] 
    two = [2400, 2450]
    three = [2500, 2550]
    four = [2600, 2650]
    
    zero = [2300, 2250]
    one = [2400, 2350] 
    two = [2500, 2450]
    three = [2600, 2550]
    four = [2700, 2650]

    ### Make array of "rocks" and index into image array ###

    layers = np.array([zero, one, two, three, four])
    model = layers[sketch]

    ### Calculate acoustic impedance ###
    
    print("Building skynthetic...")
    impedance = np.apply_along_axis(np.product, -1, model)
    print("Done")
    ref_coeff = np.diff(impedance, axis=0)

    ### Create wavelet and convolve with image ###

    w = bruges.filters.ricker(duration = 0.1, dt = 0.001, f = frequency)
    synth = np.apply_along_axis(lambda t: np.convolve(t, w, mode = 'same'), axis = 0, arr = ref_coeff)

    ### Plot ###

    im = ax[1].imshow(synth, cmap = "RdBu", aspect = 'auto', vmin = amp_min, vmax = amp_max)
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes('bottom', size = '5%', pad = 0.05)
    cbar = fig.colorbar(im, cax = cax, orientation = 'horizontal')
    cbar.set_ticks([amp_min, amp_min/2, 0, amp_max/2, amp_max])
    cbar.set_label('amplitude')
    ax[1].axes.xaxis.set_ticklabels([])
    ax[1].axes.yaxis.set_ticklabels([])
    ax[1].axes.xaxis.set_ticks([])
    ax[1].axes.yaxis.set_ticks([])

    plt.tight_layout()
    
    if output_name is not None:
        
        plt.savefig('figures/{}.jpg'.format(output_name), bbox_inches = 'tight', dpi = 96)