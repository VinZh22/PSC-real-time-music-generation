def rythme_euclidien(k, n, offset = 0):		# k des n temps sont activés. L'offset (positif) indique le décalage entre la forme avec offset et la forme de base, avec un décalage comme ceci = 100100 -> 010010 avec offset de 1
	restes = [n, k]
	while restes[-1] > 1:
		restes.append(restes[-2]%restes[-1])
	restes.pop(0)
	if restes[-1] == 0:
		L_final = restes[-2]*rythme_euclidien(k//restes[-2], n//restes[-2])
	elif k > n/2:
		L_inv01 = rythme_euclidien(n-k, n)
		L_inv = [1-e for e in L_inv01]
		L_final = [L_inv[-i-1] for i in range(n)]
	else:
		L_tot = []
		for i in range(k):
			L_tot.append([1])
		for i in range((n-k)):
			L_tot.append([0])
		while restes[0] > 1:
			for i in range(restes[0]):
				elt_liste = L_tot.pop(-restes[0]+i)
				L_tempo = [e for e in L_tot[i]]
				L_tot[i] = [e for e in L_tempo]
				for e in elt_liste:
					L_tot[i].append(e)
			restes.pop(0)
		L_final = []
		for e in L_tot:
			for f in e:
				L_final.append(f)
	L_final = 2*L_final
	L_final_offset = [0 for i in range(n)]
	for i in range(n):
		L_final_offset[i] = L_final[n+i-offset]
	return L_final_offset

def format_rythme(L):
	R = []
	if L[0] == 0:
		return format_rythme([1] + L[1:])
	for e in L:
		if e == 0:
			R[-1] += 1
		else:
			R.append(1)
	return R 
