import os
import commands
import urllib

build = 'build/'

def reformat_name(filename):
	return filename[:-4].replace('_', ' ').title().replace("'S", "'s")
	
	
filenames = [f for f in os.listdir('recipes') if f[-4:] == '.txt' and f[0] != '.']
filenames.sort(key=str.lower)

header = """
===================
S76EYTBNCCO Recipes
===================

.. contents:: **Table of Contents**
    :depth: 1
"""

recipe_header = """
`\< back to recipes <index.html>`_

"""

recipes = []

for filename in filenames:
	with open('recipes/%s' % filename) as f:
		recipe = f.read()
	name = reformat_name(filename)
	section_header = "`%s <%s.html>`_" % (name, urllib.quote(filename[:-4], safe=''))
	recipes.append((filename, "\n".join([
		section_header,
		"="*len(section_header),
		recipe
	])))

with open(build+'recipes.txt', 'w') as master:
	master.write(header+"\n\n")
	for filename, recipe in recipes:
		master.write(recipe+"\n\n")
		with open(build+filename, 'w') as recipe_file:
			recipe_file.write(recipe_header)
			recipe_file.write(recipe)
		commands.getoutput('rst2html.py "%s.txt" "%s.html" --stylesheet single.css' % ((build+filename[:-4],)*2))

commands.getoutput("rst2html.py %srecipes.txt %sindex.html --stylesheet master.css" % ((build,)*2))
commands.getoutput("rm %s*.txt" % build)

