f = open('1.txt','w')
s = 'nsfocus'
for i in range(100000):
	m = '%05d' % i
	f.write(s+m+'\n')