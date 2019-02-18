import quandl 
import csv
import pandas as pd
f = open("in.csv","w")
mydata = quandl.get("BSE/BOM500209",start_date="2000-01-3=01", end_date="2017-10-31",collapse="monthly")
mydata = pd.DataFrame(mydata)
for key in mydata:
    f.write(key)
    f.write("\n")
f.close()
print (mydata['open'])
