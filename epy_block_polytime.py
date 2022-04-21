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

    def __init__(self, kind_of_signal = "T1",number_of_segment = 4,phase_state = 2, delta_f = 2000, t_seg = 0.004, t_interval = 1e-4):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Polytime Code Vector Source',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.k = k = number_of_segment
        self.kind = kind_of_signal
        self.n = phase_state
        self.delta_f = delta_f
        self.t_interval = t_interval
        self.t_seg = 0.004
        self.T = self.t_seg * k
        self.t_vector = np.arange(0,self.T,self.t_interval)
        self.seg_len = int(len(self.t_vector)/k)
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        items = np.zeros((len(self.t_vector),2))
        if self.kind == 'T1':
            for j in range(0,self.k,1):
                for time in range(0,self.seg_len):
                    T1_theta = np.mod((2*math.pi/self.n)*math.floor((self.k*self.t_vector[(j*self.seg_len)+time]-j*self.T)*j*self.n/self.T),2*math.pi)
                    items[j*self.seg_len+time] = pol2cart(T1_theta,1)
        
        elif self.kind == 'T2':
            for j in range(0,self.k,1):
                for time in range(0,self.seg_len):
                    T2_theta = np.mod((2*math.pi/self.n)*math.floor((self.k*self.t_vector[(j*self.seg_len)+time]-j*self.T)*(2*j-self.k+1)/self.T*self.n/2),2*math.pi)
                    items[j*self.seg_len+time] = pol2cart(T2_theta,1)

        elif self.kind == 'T3':
            for j in range(0,self.k,1):
                for time in range(0,self.seg_len):
                    T3_theta = np.mod((2*math.pi/self.n)*math.floor((self.n*self.delta_f*math.pow(self.t_vector[(j*self.seg_len)+time],2))/(2*self.T)),2*math.pi)
                    items[j*self.seg_len+time] = pol2cart(T3_theta,1)

        elif self.kind == 'T4':
            for j in range(0,self.k,1):
                for time in range(0,self.seg_len):
                    T4_theta = np.mod((2*math.pi/self.n)*math.floor((self.n*self.delta_f*math.pow(self.t_vector[(j*self.seg_len)+time],2))/(2*self.T)-(self.n*self.delta_f*self.t_vector[(j*self.seg_len)+time]/2)),2*math.pi)
                    items[j*self.seg_len+time] = pol2cart(T4_theta,1)            
        
        items = np.round(items,3)
        
        for i in range(len(output_items[0])):
            output_items[0][i] = items[i%len(self.t_vector)][0]
            output_items[1][i] = items[i%len(self.t_vector)][1] 
        return len(output_items[0])
