import os
import commands

def reformat_name(filename):
	return filename[:-4].replace('_', ' ').title().replace("'S", "'s")
	
	
filenames = [f for f in os.listdir('recipes') if f[-4:] == '.txt' and f[0] != '.']
filenames.sort()

header = """
===================
S76EYTBNCCO Recipes
===================

.. contents:: Table of Contents
    :depth: 1
"""

recipe_header = """
`\< back to recipes <recipes.html>`_

"""

recipes = []

for filename in filenames:
	with open('recipes/%s' % filename) as f:
		recipe = f.read()
	#second_line = recipe.split('\n')[1]
	#if len(second_line) < 2 or second_line[:2] != "==":
	name = reformat_name(filename)
	recipes.append((filename, "\n\n".join([
		"`%s <%s.html>`_\n%s" % (name, filename[:-4], "="*(len(name)+len(filename)+7)),
		recipe
	])))

with open('recipes.txt', 'w') as master:
	master.write(header+"\n\n")
	for filename, recipe in recipes:
		master.write(recipe+"\n\n")
		with open(filename, 'w') as recipe_file:
			recipe_file.write(recipe_header)
			recipe_file.write(recipe)
		commands.getoutput('rst2html.py "%s.txt" "%s.html" --stylesheet single.css' % ((filename[:-4],)*2))

commands.getoutput("rst2html.py recipes.txt recipes.html --stylesheet master.css")
