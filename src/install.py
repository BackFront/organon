#!/usr/bin/python
#coding=utf-8

#This script makes part of Organon Project
#https://github.com/fnk0c/organon


"""
	Copyright (C) 2015  Franco Colombino & Ygor Máximo

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

__AUTHOR__ 	= "Fnkoc"
__DATE__ = "04/09/2015"

from sys import argv
from re import findall
from os import system

template = \
"""#!/bin/bash

#Move organon to /usr/share
cp -R .cache/organon /usr/share/

echo \#\!/bin/bash >> /usr/bin/organon
echo cd /usr/share/organon >> /usr/bin/organon
echo exec python organon.py \"\$\@\" >> /usr/bin/organon

chmod +x /usr/bin/organon
chmod 777 /usr/share/organon
"""

EXT = {
"python":"py",
"ruby":"rb",
"shell":"sh",
"php":"php",
"perl":"pl"
}

#Package to be install
pkg_name = argv[1]

#Store config file
pkgconfig = []

def data():
	#open, reads and append config file to list

	global INSTRUCTIONS
	global INSTALLER
	global TYPE

	with open(pkg_name + ".conf", "r") as f:
		pkgconfig_file = f.read()
		pkgconfig.append(pkgconfig_file)

	#colect data for program compilation and install
	for variables in pkgconfig:
		TYPE = findall("type = (.*)", variables)[0]
		INSTALLER = findall("installer = (.*)", variables)[0]
		INSTRUCTIONS = variables[variables.find("{") + 1:variables.find("}")]

def script_creator():
	#generates shell script to compile program

	global INSTRUCTIONS
	global INSTALLER
	global TYPE

	with open("process.sh", "w") as process:
		process.write("\
#!/bin/bash\n\n\
#This script is generated by organon\n\
" + INSTRUCTIONS.replace("\"", "").replace(",", "").replace("\t", "") +
"#end")

	system("sh process.sh")

	#Check if program need to be installed manually
	if "True" in INSTALLER:
		with open("install.sh", "w") as script:
			for n in template.replace("organon", pkg_name).replace("python", \
			TYPE).replace("py", EXT[TYPE]):
				script.write(n)
		system("sudo sh install.sh")

if __name__ == "__main__":
	try:
		data()
		script_creator()
		system("rm install.sh process.sh %s" % pkg_name)
	except Exception as e:
		print(e)
		exit()
	
