"""
Usage: python script.py source_dir extension
Eg. python3 converttowebp.py /source/folder .jpg
And it will search recursively in dir
and convert all ".jpg",".gif",".png",".jpeg" (or specified file ext) with optimized webp 
and backup originals recursively in a backup  dir.
Case-sensitive
"""
from sys import argv
import os
from PIL import Image
from pathlib import PurePath
def checkPath(source_dir):
	if not os.path.exists(source_dir):
		raise Exception("Cannot find " + source_dir)
		exit(1)

	return True
def createBackupDir(source_dir):
	p = PurePath(source_dir)
	pathsections = list(p.parts)
	pathsections.insert(-1, 'BACKED-UP-IMAGES')
	pathsections.pop()
	return PurePath('').joinpath(*pathsections)
def checkExtensions(extension):
	if not extension:
		valid_images = ['.jpg','.gif','.png','.jpeg']
	elif (extension and extension.startswith('.')):
		valid_images = []
		valid_images.append(extension)
	else:
		raise Exception('Extension must start with a .')
		exit()
	return valid_images

def convert(source_dir, extension=False):
	replaced = 0
	valid_images = checkExtensions(extension)

	print('REPLACING ALL FILES ENDING IN - ', valid_images)

	source_dir = os.path.normpath(str(source_dir.rstrip()))
	os.chdir(os.path.join(source_dir, '../'))

	source_dir = os.path.relpath(source_dir)
	backup_dir = createBackupDir(source_dir)
		
	if(checkPath(source_dir)):	
		for path, subdirs, files in os.walk(source_dir):
			for name in files:
				ext = os.path.splitext(name)[1]
				if(ext.lower() in valid_images):
					file_path = os.path.join(path,name)
					im = Image.open(file_path)
					os.makedirs(os.path.join(backup_dir,path), exist_ok=True)
					os.rename(file_path, os.path.join(backup_dir, file_path))
					print( os.path.join(backup_dir, file_path))
					im.convert('RGBA').save(file_path.replace(ext, '.webp'), 'WEBP', transparency=0)
					print(file_path, ' -> ', file_path.replace(ext, '.webp'))
					replaced +=1
		
		print('==---------- DONE (',replaced, 'Replacements) -----------==')

if len(argv) < 2:
	raise Exception('Not enough argurments')
	exit()
elif len(argv) == 2:
	script, source_dir = argv
	convert(source_dir)
elif len(argv) == 3: 
	script, source_dir, extension = argv
	convert(source_dir, extension)
else:
	raise Exception('Invalid arguments')
	exit()