names = ["clinton", "trump", "sanders"]

from sklearn.utils import shuffle
from keras import Sequential
from keras.layers import Dropout, LSTM, Dense
import numpy as np
from keras.utils import to_categorical

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

train_tweets = []
train_labels = []

for i in range(len(names)):
	fp = open("../data/" + names[i] + "_train.txt", "r")
	clinton_tweets = fp.readlines()
	add_tweets(clinton_tweets, train_tweets)
	fp.close()
	train_labels += [i] * len(clinton_tweets)

train_tweets, train_labels = shuffle(train_tweets, train_labels)
train_outputs = to_categorical(train_labels)

for i in range(len(train_tweets)):
	train_tweets[i] = np.array(train_tweets[i])

model = Sequential()
model.add(LSTM(90, input_shape=(None, input_len), recurrent_dropout=0.2))
model.add(Dropout(0.3))
model.add(Dense(30, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(len(names), activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(np.array(train_tweets), np.array(train_outputs), epochs=70, batch_size=20)

model.save("../models/model.h5")
