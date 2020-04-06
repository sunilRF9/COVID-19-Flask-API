import os
cmd = 'curl http://localhost:1111/json/india/'
for _ in range(50):
    print(os.system(cmd))
    
