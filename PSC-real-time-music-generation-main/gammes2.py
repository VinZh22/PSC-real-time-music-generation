"""elements solfège basiques"""

def nombre_lettre(n):
	n0 = n%12
	m = n//12
	if n0 == 0:
		return "A"
	elif n0 == 1:
		return "A#"
	elif n0 == 2:
		return "B"
	elif n0 == 3:
		return "C"
	elif n0 == 4:
		return "C#"
	elif n0 == 5:
		return "D"
	elif n0 == 6:
		return "D#"
	elif n0 == 7:
		return "E"
	elif n0 == 8:
		return "F"
	elif n0 == 9:
		return "F#"
	elif n0 == 10:
		return "G"
	else:
		return "G#"

def lettre_nombre(L):
	if L == "A":
		return 0
	elif L == "A#" or L == "Bb":
		return 1
	elif L == "B":
		return 2
	elif L == "C":
		return 3
	elif L == "C#" or L == "Db":
		return 4
	elif L == "D":
		return 5
	elif L == "D#" or L == "Eb":
		return 6
	elif L == "E":
		return 7
	elif L == "F":
		return 8
	elif L == "F#" or L == "Gb":
		return 9
	elif L == "G":
		return 10
	elif L == "G#" or L == "Ab":
		return 11
	else :
		print("error gammes.lettre_nombre", L)
		return 0


def gamme(root = "A", mode = "Major"):
	n = lettre_nombre(root)
	R = [n]
	pattern = 0
	while R[0] >= 0:
		if mode == "Major":
			if pattern == 0 or pattern == 4:
				R = [R[0]-1]+R
			else:
				R = [R[0]-2]+R
		elif mode == "Natural Minor":
			if pattern == 2 or pattern == 5:
				R = [R[0]-1]+R
			else:
				R = [R[0]-2]+R
		elif mode == "Harmonic Minor":
			if pattern == 0 or pattern == 2 or pattern == 5:
				R = [R[0]-1]+R
			elif pattern == 1:
				R = [R[0]-3]+R
			else:
				R = [R[0]-2]+R
		elif mode == "Melodic Minor":
			if pattern == 0 or pattern == 5:
				R = [R[0]-1]+R
			else:
				R = [R[0]-2]+R
		if pattern == 6:
			pattern = 0
		else:
			pattern += 1
	R.pop(0)
	pattern = 0
	while R[-1] <= 88:
		if mode == "Major":
			if pattern == 2 or pattern == 6:
				R.append(R[-1]+1)
			else:
				R.append(R[-1]+2)
		elif mode == "Natural Minor":
			if pattern == 1 or pattern == 4:
				R.append(R[-1]+1)
			else:
				R.append(R[-1]+2)
		elif mode == "Harmonic Minor":
			if pattern == 1 or pattern == 4 or pattern == 6:
				R.append(R[-1]+1)
			elif pattern == 5:
				R.append(R[-1]+3)
			else:
				R.append(R[-1]+2)
		elif mode == "Melodic Minor":
			if pattern == 1 or pattern == 6:
				R.append(R[-1]+1)
			else:
				R.append(R[-1]+2)
		if pattern == 6:
			pattern = 0
		else:
			pattern += 1
	R.pop(-1)
	return R



def accord(root = "A", quality = "Major", seventh = "Dominant"):
	"""
	root = racine de l'accord, note de base; peut être avec un dièse, bémol,...
	quality = "Major", "Minor", "Augmented", "Diminished", "Seventh"
	seventh = "Dominant", "Major", "Minor", "Half-diminished", "Diminished", "Minor-major", "Augmented-major", "Augmented". Utile que si quality = "Seventh"
	"""
	n = lettre_nombre(root)
	R = [n]
	pattern = 0
	while R[0] >= 0:
		if quality == "Major" or (quality == "Seventh" and seventh == "Dominant") or (quality == "Seventh" and seventh == "Major"):
			if pattern == 0:
				R = [R[0]-5]+R
			elif pattern == 1:
				R = [R[0]-3] + R
			else:
				R = [R[0]-4] + R
		elif quality == "Minor" or (quality == "Seventh" and seventh == "Minor") or (quality == "Seventh" and seventh == "Minor-major"):
			if pattern == 0:
				R = [R[0]-5]+R
			elif pattern == 1:
				R = [R[0]-4] + R
			else:
				R = [R[0]-3] + R
		elif quality == "Augmented" or (quality == "Seventh" and seventh == "Augmented-major") or (quality == "Seventh" and seventh == "Augmented"):
			if pattern == 0:
				R = [R[0]-4]+R
			elif pattern == 1:
				R = [R[0]-4] + R
			else:
				R = [R[0]-4] + R
		elif quality == "Diminished" or (quality == "Seventh" and seventh == "Half-diminished") or (quality == "Seventh" and seventh == "Diminished"):
			if pattern == 0:
				R = [R[0]-6]+R
			elif pattern == 1:
				R = [R[0]-3] + R
			else:
				R = [R[0]-3] + R
	R.pop(0)
	pattern = 0
	while R[-1] <= 88:
		if quality == "Major" or (quality == "Seventh" and seventh == "Dominant") or (quality == "Seventh" and seventh == "Major"):
			if pattern == 0:
				R.append(R[-1]+4)
			elif pattern == 1:
				R.append(R[-1]+3)
			else:
				R.append(R[-1]+5)
		elif quality == "Minor" or (quality == "Seventh" and seventh == "Minor") or (quality == "Seventh" and seventh == "Minor-major"):
			if pattern == 0:
				R.append(R[-1]+3)
			elif pattern == 1:
				R.append(R[-1]+4)
			else:
				R.append(R[-1]+5)
		elif quality == "Augmented" or (quality == "Seventh" and seventh == "Augmented-major") or (quality == "Seventh" and seventh == "Augmented"):
			if pattern == 0:
				R.append(R[-1]+4)
			elif pattern == 1:
				R.append(R[-1]+4)
			else:
				R.append(R[-1]+4)
		elif quality == "Diminished" or (quality == "Seventh" and seventh == "Half-diminished") or (quality == "Seventh" and seventh == "Diminished"):
			if pattern == 0:
				R.append(R[-1]+3)
			elif pattern == 1:
				R.append(R[-1]+3)
			else:
				R.append(R[-1]+6)
		if pattern == 2:
			pattern = 0
		else:
			pattern += 1
	R.pop(-1)
	if quality == "Seventh":
		if (seventh == "Major" or seventh == "Minor-major" or seventh == "Augmented-major") and n-1 >= 0:
			R.append(n-1)
		elif (seventh == "Dominant" or seventh == "Minor" or seventh == "Half-diminished" or seventh == "Augmented") and n-2 >= 0:
			R.append(n-2)
		elif seventh == "Diminished" and n-3 >= 0:
			R.append(n-3)
		if (seventh == "Major" or seventh == "Minor-major" or seventh == "Augmented-major"):
			i = 0
			while n+11+(12*i) <= 88:
				R.append(n+11+(12*i))
				i += 1
		elif (seventh == "Dominant" or seventh == "Minor" or seventh == "Half-diminished" or seventh == "Augmented"):
			i = 0
			while n+10+(12*i) <= 88:
				R.append(n+10+(12*i))
				i += 1
		elif seventh == "Diminished":
			i = 0
			while n+9+(12*i) <= 88:
				R.append(n+9+(12*i))
				i += 1
	R.sort()
	return R



