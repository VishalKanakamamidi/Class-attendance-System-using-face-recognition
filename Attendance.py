import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

f = open("vishal.csv","r")
k = f.readlines()
Subject = ["SB","BA","BB","ACJ","SM","MC"]
objects = ["SB","BA","BB","ACJ","SM","MC"]
Total = [0]*6
Present = [0]*6
Att = list()

for i in k:
	a = i.split(",")
	b = a[1].split(" ")
	c = a[2].split(" ")
	
	for j in range(0,6):
		for l in b:
			if(Subject[j] == l):
				Total[j] = Total[j]+1

		for m in c:
			if(Subject[j] == m):
				Total[j] = Total[j]+1
				Present[j] = Present[j]+1


for i in range(0,6):
	a = Present[i]/Total[i]
	a = a*100
	a = int(a)
	objects[i] = objects[i]+" "+str(a)
	Att.append(a)

y_pos = np.arange(len(objects))
plt.bar(y_pos, Att, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Attendance')
plt.title('Subject')

plt.show()



