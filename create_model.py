from sklearn.utils import shuffle
from keras import Sequential
from keras.layers import Dropout, LSTM, Dense
import numpy as np

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

fp = open("clinton_train.txt", "r")
clinton_tweets = fp.readlines()
add_tweets(clinton_tweets, train_tweets)
fp.close()
train_outputs += [0] * len(clinton_tweets)
fp = open("trump_train.txt", "r")
trump_tweets = fp.readlines()
add_tweets(trump_tweets, train_tweets)
fp.close()
train_outputs += [1] * len(trump_tweets)

train_tweets, train_outputs = shuffle(train_tweets, train_outputs)

for i in range(len(train_tweets)):
	train_tweets[i] = np.array(train_tweets[i])

model = Sequential()
model.add(LSTM(70, input_shape=(None, 88)))
model.add(Dropout(0.5))
model.add(Dense(30, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(1, activation="sigmoid"))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=["accuracy"])
model.fit(np.array(train_tweets), np.array(train_outputs), epochs=70, batch_size=20)

model.save("model.h5")
