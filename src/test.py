names = ["clinton", "trump", "sanders"]

from keras.models import load_model
import numpy as np

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

test_tweets = []
test_labels = []

all_tweets = []

for i in range(len(names)):
	fp = open("../data/" + names[i] + "_test.txt", "r")
	tweets = fp.readlines()
	add_tweets(tweets, test_tweets)
	all_tweets += tweets
	fp.close()
	test_labels += [i] * len(tweets)

right = 0
wrong = 0
results = model.predict(np.array(test_tweets))
for i in range(len(test_tweets)):
	correct = True
	for j in range(len(names)):
		if j != test_labels[i] and results[i][j] >= results[i][test_labels[i]]:
			correct = False
	if correct:
		right += 1
	else:
		wrong += 1

print("Accuracy:", right / (right + wrong))
