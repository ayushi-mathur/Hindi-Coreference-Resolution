from os import listdir, system
from os.path import isfile, join
import random
onlyfiles = [f for f in listdir("./data/") if isfile(join("./data/", f))]
random.shuffle(onlyfiles)

system("rm -rf ./testingdata")
system("rm -rf ./trainingdata")
system("mkdir ./trainingdata")
system("mkdir ./testingdata")


for index,i in enumerate(onlyfiles):
    if index < 2*len(onlyfiles)/3:
        system(f"cp ./data/{i} ./trainingdata/{i}")
    else:
        system(f"cp ./data/{i} ./testingdata/{i}")
