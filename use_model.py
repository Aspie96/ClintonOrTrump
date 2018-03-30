import numpy as np
from keras.models import load_model

dictionary = [" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "=", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "|", "~"]

def add_tweets(tweets, output):
	for tweet in tweets:
		sequence = [[0] * len(dictionary)] * (150 - len(tweet))
		for c in tweet:
			if c in dictionary:
				array = [0] * len(dictionary)
				array[dictionary.index(c)] = 1
				sequence += [array]
			else:
				sequence = [[0] * len(dictionary)] + sequence
		output.append(sequence)

train_tweets = []
train_outputs = []

model = load_model("model.h5")

repeat = True
while repeat:
	tweet = input("tweet> ")
	if tweet == "exit":
		repeat = False
	else:
		tweets = []
		add_tweets([tweet], tweets)
		output = model.predict(np.array(tweets))[0]
		if output > 0.5:
			label = "Trump"
		else:
			label = "Clinton"
		print(output, label)
