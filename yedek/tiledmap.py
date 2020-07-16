def isPelindrom(n):
	num = str(n)
	assert num.isalnum() == True
	return num == num[::-1]


print(isPelindrom("122s1"))