"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import math

def pol2cart(theta,rho):
    x =rho * math.cos(theta)
    y =rho * math.sin(theta)
    return x, y



class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, code_length = 16, kind_of_signal = "Frank"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Polyphase Code Vector Source',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.code_length = code_length
        self.kind = kind_of_signal
    def work(self, input_items,output_items):
        """example: multiply with constant"""

        freq_step = int(self.code_length ** (1/2))

        if freq_step**2 != self.code_length:
            print("Square root of code Length is not integer.")
            exit()
            
        delta_pi = math.pi / freq_step
        delta_pi_2 = math.pi / self.code_length

        items = np.zeros((self.code_length,2))

        if self.kind == "Frank":
            for j in range(1,freq_step+1):
                for i in range(1,freq_step+1):
                    frank_theta = 2*(i-1)*(j-1)*delta_pi
                    items[(i-1)+(j-1)*freq_step] = pol2cart(frank_theta, 1)

        elif self.kind == "P1":
            for j in range(1,freq_step+1):
                for i in range(1,freq_step+1):
                    P1_theta = -(freq_step-(2*j-1))*((j-1)*freq_step+(i-1))*delta_pi
                    items[(i-1)+(j-1)*freq_step] = pol2cart(P1_theta,1)

        elif self.kind == "P2":
            for j in range(1,freq_step+1):
                for i in range(1,freq_step+1):
                    P2_theta = 2*delta_pi*((freq_step+1)/2-i)*((freq_step+1)/2-j)
                    items[(i-1)+(j-1)*freq_step] = pol2cart(P2_theta,1)                    

        elif self.kind == "P3":
            for i in range(1,self.code_length+1):
                P3_theta = ((i-1)*(i-1))*delta_pi_2
                items[i-1] = pol2cart(P3_theta,1)
                #print(P3_theta)

        elif self.kind == "P4":
            for i in range(1,self.code_length+1):
                P4_theta = (i-1)*(i-1-self.code_length)*delta_pi_2
                items[i-1] = pol2cart(P4_theta,1)
                #print(P4_theta)            
        items = np.round(items,3)
        #print("items = {}".format(items))
        for i in range(len(output_items[0])):
            output_items[0][i] = items[i%self.code_length][0]
            output_items[1][i] = items[i%self.code_length][1] 
        return len(output_items[0])

