#n = 7 vaut le 7 diminué et n = 8 vaut le 7 majeur pour la gamme mineure
import numpy.random as rd

def nb_suiv(gamme = "Major", n = 1):
	if gamme == "Major":
		if n == 1:
			return rd.choice([2, 3, 4, 5, 6, 7])
		elif n == 2 or n == 4:
			return rd.choice([5, 7])
		elif n == 3:
			return 6
		elif n == 5:
			return 1
		elif n == 6:
			return rd.choice([2, 4])
		elif n == 7:
			return rd.choice([1, 3])
		else:
			print("erreur nb_suivi", gamme, n)
	elif gamme == "Minor":
		if n == 1:
			return rd.choice([2, 3, 4, 5, 6, 7])
		elif n == 2:
			return rd.choice([5, 7])
		elif n == 3:
			return 6
		elif n == 4:
			return rd.choice([5, 7, 8])
		elif n == 5 or n == 7:
			return 1
		elif n == 6:
			return rd.choice([2, 4])
		elif n == 8:
			return 3
		else:
			print("erreur nb_suivi", gamme, n)
	else:
			print("erreur nb_suivi", gamme, n)


def acc_suivi(root_init, qual_init, n):
	L = []
	if root_init == 'A':
		L = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
	elif root_init == 'B':
		L = ['B', 'C', 'D', 'E', 'F', 'G','A']
	elif root_init == 'C':
		L = ['C', 'D', 'E', 'F', 'G','A', 'B']
	elif root_init == 'D':
		L = ['D', 'E', 'F', 'G','A', 'B', 'C']
	elif root_init == 'E':
		L = ['E', 'F', 'G','A', 'B', 'C', 'D']
	elif root_init == 'F':
		L = ['F', 'G','A', 'B', 'C', 'D', 'E']
	elif root_init == 'G':
		L = ['G','A', 'B', 'C', 'D', 'E', 'F']
	else:
		print("erreur acc_suivi")
	root_fin = L[(n-1)%len(L)]
	qual_fin = ''
	if qual_init == 'Major':
		if n == 1:
			qual_fin = 'Major'
		elif n == 2:
			qual_fin = 'Minor'
		elif n == 3:
			qual_fin = 'Minor'
		elif n == 4:
			qual_fin = 'Major'
		elif n == 5:
			qual_fin = 'Major'
		elif n == 6:
			qual_fin = 'Minor'
		elif n == 7:
			qual_fin = "Diminished"
		else:
			print("erreur acc_suivi")
	elif qual_init == 'Minor':
		if n == 1:
			qual_fin = 'Minor'
		elif n == 2:
			qual_fin = 'Diminished'
		elif n == 3:
			qual_fin = 'Major'
		elif n == 4:
			qual_fin = 'Minor'
		elif n == 5:
			qual_fin = 'Major'
		elif n == 6:
			qual_fin = 'Major'
		elif n == 7:
			qual_fin = 'Diminished'
		elif n == 8:
			qual_fin = 'Major'
		else:
			print("erreur acc_suivi")
	else:
		print("erreur acc_suivi")
	return (root_fin, qual_fin)


