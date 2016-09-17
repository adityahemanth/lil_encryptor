# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


# module to encrypt text into image
# and vice versa.

# [START imports]
import sys, math
from PIL import Image, ImageDraw
# [END imports]


# [START Encrypter]
class Encrypter:


	# empty constructor
	def __init__(self):
		pass


	# helper methods
	def _reader(self,file):
		for line in open(file):
			for char in line:
				yield char



	def _get_color(self,file):
		color = []
		for chr in self._reader(file):
			color.append( hex(ord(chr)).upper()[2:].zfill(2) )
			if len(color) == 3:
				yield '#' + reduce( lambda x, y : x + y, color)
				color = []


	def _to_word(self, color):
		word = ''
		for x in color:
			word += chr(x)
		return word



	# decrypts encrypted text files
	# needs to be able to be a square image to 
	# be able it to be encrypted and decrypted.

	def decrypt(self, img, output = None):
		im = Image.open(img)
		print im.size
		[resx, resy] = im.size
		rgb_im = im.convert('RGB')

		if output == None:
			output = img.split('.')[0] + '.txt'

		with open(output, 'w') as board:
			for i in xrange(0, resx):
				for j in xrange(0, resy):
					board.write(self._to_word(rgb_im.getpixel((i, j))))





	# encrypts the text file (file) into an image
	# it does this by storing each char as a color
	# value in the image
	def encrypt(self, file, save=None, step=1):

		words =  (word for word in open(file))
		w_len = reduce( lambda x , y : x + y, map(lambda x : len(x), words))
		resx = resy = int(math.ceil(math.sqrt(w_len/3)))

		im = Image.new('RGBA', [resx, resy], (255,255,255,0))
		draw = ImageDraw.Draw(im)

		colors = self._get_color(file)
		for i in xrange(0, resx, step):
			for j in xrange(0, resy, step):

				try:
					color = colors.next()
				except:
					break

				draw.rectangle([(i,j),(i+step, j+step)], fill= color, outline=color)

		del draw
		if save == None:
			save = file.split('.')[0] + '.png'

		im.save(save, "PNG")

# [END Encrypter]
