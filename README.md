# Movies rating analyzing
Analyzing and predicting a moveis's rating using data scrape from IMDB
## Running instructions
First, run this code in these commands in 2 seperated terminal (command prompt):
```
pyspark
```
```
spark-shell
```
Then, cd to the kafka folder and rung the following codes in seperated terminal as well:
```
bin\windows\zookeeper-server-start config\zookeeper.properties
```
```
bin\windows\kafka-server-start config\server.properties
```
Lastly, cd to the repo clone and run `pip install requirements.txt` to install the required packages.
