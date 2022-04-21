"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, primitive_root = 2, prime_number = 11):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Costas Code Vector Source',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.root = primitive_root
        self.number = prime_number
        
    def work(self, input_items,output_items):
        """example: multiply with constant"""
        items = []
        multiply_const = int(100*(self.number-1))        
        for i in range(1, self.number):
            items = np.r_[items, (self.root ** i) % self.number] 
        
        items = items * multiply_const
        for i in range(len(output_items[0])):
            output_items[0][i] = items[i%(self.number-1)] 
        return len(output_items[0])
