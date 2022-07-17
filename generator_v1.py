from ast import Pass
from transmitter import transmitters
from gnuradio import channels, gr, blocks
import numpy as np
import numpy.fft
import random
import time
import pickle
import math

'''
Generate dataset with dynamic channel model across range of SNRs
'''

apply_channel = True

dataset = {}

# The output format looks like this
# {('mod type', SNR): np.array(nvecs_per_key, 2, vec_length), etc}

nvecs_per_key = 200
vec_length = 1024
samp_rate = 2e6
snr_vals = range(-20,12,2)

# radar signal parameters
code_length = [7,11,13]
LFM_amp = np.arange(0.5,2,0.5)
polyphase_code_len = [16,25,36,64]
polytime_segment = [4,5,6]
polytime_B = [2000,4000,6000]

for snr in snr_vals:
    print("snr is {}".format(snr))
    for fmcw_type in transmitters.keys():
        print("now encoded signal is ..{}".format(fmcw_type))
        for i,mod_type in enumerate(transmitters[fmcw_type]):
            dataset[(mod_type.modname, snr)] = np.zeros([nvecs_per_key,2,vec_length], dtype=np.float32)
            # moar vectors!
            insufficient_modsnr_vectors = True
            modvec_indx = 0
            while insufficient_modsnr_vectors:
                if fmcw_type == "FMCW_LFM":
                    src_mod = mod_type(amp=random.choice(LFM_amp),offset=0,samp_rate=samp_rate)
                elif fmcw_type == "FMCW_Barker":
                    src_mod = mod_type(code_length = random.choice(code_length))
                elif fmcw_type == "FMCW_Costas":
                    src_mod = mod_type(prime_number=11, primitive_root=2, samp_rate=samp_rate)
                elif fmcw_type == "FMCW_Polyphase":
                    src_mod = mod_type(signal_freq = samp_rate/20,code_length = random.choice(polyphase_code_len),kind_of_signal = mod_type.modname)
                elif fmcw_type == "FMCW_Polytime":
                    src_mod = mod_type(Kind_of_signal = mod_type.modname,delta_f=random.choice(polytime_B) , phase_state = 2, segment = random.choice(polytime_segment))
                # print(src_mod)
                fD = 0
                # delays = [0.0, 0.9, 1.7]
                delays = [0.0]
                # mags = [1, 0.8, 0.3]
                mags = [0]
                ntaps = 1
                # ntaps = 0
                noise_amp = 10**(-snr/10.0)
                chan = channels.channel_model(
                noise_voltage=math.sqrt(noise_amp),
                frequency_offset=0.0,
                epsilon=1,
                taps=[1],
                noise_seed=10,
                block_tags=False)
                # chan = channels.dynamic_channel_model(
                #     200e3,  # samp rate
                #     0.01,   # SRO Standard Deviation Hz per sample
                #     0,     # Max SRO Bound Hz
                #     .01,    # CFO Standard Deviation Hz per sample
                #     0.5e3,  # Max CFO Bound Hz
                #     0,      # Num Sinusoids(SoS model)
                #     fD,     # Max Doppler Freq(Hz)
                #     True,   # LOS/Rician(True) , NLOS/Rayleigh(False)
                #     0,      # K : Rician K-factor, the ratio of specular to diffuse power in the model
                #     delays, # delays : A list of fractional sample delays making up the power delay profile
                #     mags,   # mags : A list of magnitudes corresponding to each delay time in the power delay profile
                #     ntaps,  # ntaps_mpath : The length of the filter to interpolate the power delay profile over. Delays in the PDP
                #     noise_amp, # noise_amp : Specifies the standard deviation of the AWGN process
                #     0x1337) #    noise_seed : A random number generator seed for the noise source.
                # print("check...1")
                snk = blocks.vector_sink_c()
                # print("check...2")
                tb = gr.top_block()
                # connect blocks
                if apply_channel:
                    tb.connect(src_mod,chan,snk)
                else:
                    tb.connect(src_mod,snk)
                # print("check...3")
                # tb.start()
                # time.sleep(0.01)
                # tb.stop()
                tb.run()
                # del tb
                raw_output_vector = np.array(snk.data(), dtype=np.complex64)
                # print(raw_output_vector.shape)
                # start the sampler some random time after channel model transients (arbitray values here)
                sampler_indx = random.randint(50,500)
                while sampler_indx + vec_length < len(raw_output_vector) and modvec_indx < nvecs_per_key:
                    sampled_vector = raw_output_vector[sampler_indx:sampler_indx+vec_length]
                    energy = np.sum((np.abs(sampled_vector)))
                    sampled_vector = sampled_vector / energy
                    dataset[(mod_type.modname, snr)][modvec_indx,0,:] = np.real(sampled_vector)
                    dataset[(mod_type.modname, snr)][modvec_indx,1,:] = np.imag(sampled_vector)
                    sampler_indx += random.randint(vec_length, round(len(raw_output_vector)*.5))
                    modvec_indx += 1
                if modvec_indx == nvecs_per_key:
                    # we're all done
                    insufficient_modsnr_vectors = False


print("all done. writing to disk")
with open('/home/wjyun/FMCW_Classification/FMCW_RADAR2022_dict_v_change.pkl','wb') as f:
    pickle.dump(dataset, f)

