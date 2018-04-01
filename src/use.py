names = ["Clinton", "Trump", "Sanders"]

import numpy as np
from keras.models import load_model

dictionary = [" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "=", "?", "@", "[", "]", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "|", "~"]
  
input_len = len(dictionary) + 2

def add_tweets(tweets, output):
	padding = [0] * input_len
	padding[0] = 1
	for tweet in tweets:
		sequence = [padding] * (150 - len(tweet))
		for c in tweet:
			if c in dictionary:
				array = [0] * input_len
				array[dictionary.index(c) + 1] = 1
				sequence += [array]
			elif "A" <= c <= "Z":
				array = [0] * input_len
				array[dictionary.index(c.lower()) + 1] = 1
				array[input_len - 1] = 1
				sequence += [array]
			else:
				sequence = [padding] + sequence
		output.append(sequence)

model = load_model("../models/model.h5")

repeat = True
while repeat:
	tweet = input("tweet> ")
	if tweet == "exit":
		repeat = False
	else:
		tweets = []
		add_tweets([tweet], tweets)
		output = model.predict(np.array(tweets))
		a = []
		maximum = 0
		for i in range(1, len(names)):
			if output[0][i] > output[0][maximum]:
				maximum = i
		print(output[0][maximum], names[maximum])
