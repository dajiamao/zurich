#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:20:14 2017

@author: ltafm
"""
import zhinst.ziPython, zhinst.utils
import matplotlib.pyplot as plt
import pickle
import numpy as np
import math
import time
import sys

# Plot data coming from the zhinst sweeper module -- modified hg
def plot_sweeper_data2(mypath, timestr, d, Blocking=True):
  path = '/dev384/demods/0/sample'
  samples = d[path]
  # Plot
  plt.clf()
  for i in range(0, len(samples)):
    frequency = samples[i][0]['frequency']
    R = np.abs(samples[i][0]['x'] + 1j*samples[i][0]['y'])
    phi = np.angle(samples[i][0]['x'] + 1j*samples[i][0]['y'])
    plt.subplot(2, 1, 1)
    plt.semilogy(frequency, R)
    plt.subplot(2, 1, 2)
    plt.plot(frequency, phi)
    plt.subplot(2, 1, 1)
    plt.title('Results of %d sweeps.' % len(samples))
    plt.grid(True)
    plt.ylabel(r'Demodulator R ($V_\mathrm{RMS}$)')
    plt.subplot(2, 1, 2)
    plt.grid(True)
    plt.xlabel('Frequency ($Hz$)')
    plt.ylabel(r'Demodulator Phi (radians)')
    plt.autoscale()
    plt.draw()
    if Blocking:
        plt.show(block=Blocking)
    else:
        plt.savefig(mypath+'/'+timestr+'_sweeper_curve.png')
        
# Measure Quality factor

def quality_factor_from_phase2(mypath,timestr,d):
  path = '/dev384/demods/0/sample'
  samples = d[path]
  # Plot
  #plt.clf()
  for i in range(0, len(samples)):
    frequency = samples[i][0]['frequency']
    R = np.abs(samples[i][0]['x'] + 1j*samples[i][0]['y'])
    phi = np.angle(samples[i][0]['x'] + 1j*samples[i][0]['y'])
    Q = np.abs(np.diff(phi)/np.diff(frequency)*frequency[1:]/2)
    plt.figure() #make a new instance of a figure
    plt.scatter(frequency[1:], Q)
    print("Q factor: %f" % np.max(Q))
    plt.savefig(mypath+'/'+timestr+'_Q_curve.png')
    plt.show()
    
    #logging information into .txt file 
    f= open(mypath+'/'+timestr+'_log.txt','w+')
    #f= open('test_log.txt','w+')
    f.write('%s \n %s \n' % ('date: ' + timestr,'Q factor = ' + str(np.max(Q))))
    f.close
    print('data log saved to :'+mypath)

   
# Set advisor settings for Zurich Instrument's PLL
def set_pll_advisor(f0,Q):
    print("Not implemented yet")
    #sweeper.set('sweep/device',dev)
    
if __name__ == "__main__":
  data = pickle.load(open(sys.argv[1],'r'))
  quality_factor_from_phase(data) 
  plot_sweeper_data(data)
  #save_figure(data,sys.argv[1] + ".png")
  
  
