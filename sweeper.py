import zhinst.ziPython, zhinst.utils
import time
import os
import os.path
import pickle
from sweeper_utils import *
import pandas as pd
#from test_functions.py import *


# Open connection to ziServer
daq = zhinst.ziPython.ziDAQServer('localhost', 8005)

# Turn on debug logging
daq.setDebugLevel(3)

# Detect device
dev = zhinst.utils.autoDetect(daq)

# TODO: Turn off PLL otherwise it prevents the sweeper to progress
daq.setInt('/dev384/plls/0/enable', 0)

start = time.time()
timestr = time.strftime("%Y%m%d-%H%M%S") #time of operation

# making new directory to save data for each run
mypath = '/home/ltafm/lt-afm/instruments/zhinst/sweeper/data2/'+timestr
if not os.path.isdir(mypath):
   os.makedirs(mypath)

#save current settings   
zhinst.utils.save_settings(daq, dev, mypath+'/'+ timestr+'_current_settings.xml')


# Prepare sweep options
sweeper = daq.sweep()
sweeper.set('sweep/device',dev)
sweeper.set('sweep/gridnode', 'oscs/0/freq') # What to sweep
sweeper.set('sweep/start',99E3) #starting frequency
sweeper.set('sweep/stop',101E3) #ending frequency
sweeper.set('sweep/samplecount',25) #set number of data points
sweeper.set('sweep/fileformat',1)
loopcount = 1
sweeper.set('sweep/loopcount', loopcount)
path = '/%s/demods/%d/sample' % (dev, 0)
sweeper.subscribe(path)

daq.sync()
sweeper.execute()


#build empty data frame to hold data
df=pd.DataFrame({
              "Frequency": [],
              "Amplitude": []
})

   
while not sweeper.finished():  # Wait until the sweep is complete
    time.sleep(1)
    progress = sweeper.progress()
    print("Individual sweep progress: {:.2%}.".format(progress[0]))

    data = sweeper.read(True)
    if path in data:
        print("Available data")
        a=data
        freq=data["/dev384/demods/0/sample"][0][0]["frequency"]
        r=data["/dev384/demods/0/sample"][0][0]["r"]
        df_latest = pd.DataFrame({
                           "Frequency": freq,
                           "Amplitude": r
                         })
        #df_latest.to_csv('test.csv', columns=["Frequency","Amplitude"],mode='w')

        #df = df.append(df_latest)
        pickle.dump(data,open('progress.p','w'))
        #plot_sweeper_data(data, False) # plot data, blocking = False
        
        plot_sweeper_data2(mypath,timestr,data, False) # plot data, blocking = False
      
 #write csv file to time stamped file name
df_latest.to_csv(mypath+'/'+timestr+'.csv', columns=["Frequency","Amplitude"],mode='w')

#not necessary, throws error
#return_flat_dict = True
#data = sweeper.read(return_flat_dict)

# Save final data
filename = os.path.join('data',timestr + '.p')
pickle.dump(data,open(filename,'w'))

print("Output in %s" % filename)
print("CSV output in %s" % mypath)

# run q factor analysis
quality_factor_from_phase2(mypath, timestr, data)

#sweeper.set('sweep/directory', 'res_curve') # Destination folder
#directory = os.path.join('res_curve',timestr) # Folder
#if not os.path.exists(directory):
#    os.makedirs(directory)
#sweeper.save(timestr) # Save file


sweeper.unsubscribe(path)
# Stop the sweeper thread and clear the memory.
sweeper.clear()

#%%


#%%
