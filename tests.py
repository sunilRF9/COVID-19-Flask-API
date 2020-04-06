import numpy as np
import os
import time
import random
tm = []
for i in range(10):
    st = time.time()
    #port = randint(3002, 3012)
    countries = ['india','pakistan','egypt','ireland','australia','namibia','kenya','germany','poland']
    
    port = random.choice(countries) 
    cmd = 'wget "http://localhost:5000/json/' + str(port) + ' " -O /dev/null '
    print(cmd)
    os.system(cmd)
    ed = time.time()
    tm.append(ed-st)

print (np.mean(tm), np.median(tm), np.sum(tm))

