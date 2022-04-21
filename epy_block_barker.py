"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from gnuradio import blocks

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, code_length = 2):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Barker Code Vector Source',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.code_length = code_length

    def work(self, input_items,output_items):
        """example: multiply with constant"""

        if self.code_length == 2:
            items = np.array([1,-1])
        elif self.code_length == 3:
            items = np.array([1,1,-1])
        elif self.code_length == 4:
            items = np.array([1,1,-1, 1])
        elif self.code_length == 5:
            items = np.array([1,1,1,-1,1])            
        elif self.code_length == 7:
            items = np.array([1,1,1,-1,-1,1,-1]) 
        elif self.code_length == 11:
            items = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])            
        elif self.code_length == 13:             
            items = np.array([1,1,1,1,1,-1,-1,1,1,-1,1,-1,1])
            
        for i in range(len(output_items[0])):
            output_items[0][i] = items[i%self.code_length] 
        return len(output_items[0])
