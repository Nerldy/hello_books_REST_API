l = [1, 2, 3, 89]
c = [1, 2, 3]

for g in c:
	if g not in c:
		print(f"{g} nop")
	else:
		print('yeah')
