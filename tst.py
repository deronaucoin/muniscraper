import itertools

text = "congested btwn Van Ness and Embarcadero"

combos = itertools.combinations(text.split(),2)

print tuple(combos)