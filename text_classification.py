import tensorflow as tf
from tensorflow import keras
import numpy as np

data = keras.datasets.imdb

(train_data , train_labels) , (test_data , test_labels) = data.load_data(num_words=88000)

print("--------------------------datas-----------------------------------")
print(" ")
print(train_data[0])
print(train_labels[0])
print(test_data[0])
print(test_labels[0])
print(" ")

word_index = data.get_word_index()

word_index = {k:(v+3) for k,v in word_index.items() }

word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value , key) for (key , value) in word_index.items()])


train_data = keras.preprocessing.sequence.pad_sequences( train_data , value=word_index["<PAD>"] , padding="post" , maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences( test_data , value=word_index["<PAD>"] , padding="post" , maxlen=250)




def decode_review(text): 
    return " ".join([reverse_word_index.get(i , "?") for i in text])

# print(decode_review(test_data[0]))
# print(len(test_data) , len(train_data))

# model = keras.Sequential()

# model.add(keras.layers.Embedding(88000 , 16))
# model.add(keras.layers.GlobalAveragePooling1D())
# model.add(keras.layers.Dense(16  , activation="relu"))
# model.add(keras.layers.Dense(1 , activation="sigmoid"))


# model.summary()

# model.compile(optimizer="adam" ,loss="binary_crossentropy" , metrics=["accuracy"])

# x_val = train_data[:10000]
# x_train = train_data[10000:]


# y_val = train_labels[:10000]
# y_train = train_labels[10000:]

# fitModel = model.fit(x_train , y_train , epochs=40 , batch_size=512 , validation_data=(x_val , y_val) ,verbose=1)

# result = model.evaluate(test_data , test_labels )

# print(result)

model = keras.models.load_model("model.h5")
test_review = test_data[0]
predict = model.predict([test_review])
print("Review : ")
print(decode_review(test_review))
x = np.argmax(predict[0])
print("Prediction : " + str(x))
print("Actual : " + str(test_labels[0]))

model.save("model.h5")

def review_encode(s):
	encoded = [1]

	for word in s:
		if word.lower() in word_index:
			encoded.append(word_index[word.lower()])
		else:
			encoded.append(2)

	return encoded

with open("test.txt", encoding="utf-8") as f:
	for line in f.readlines():
		nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"","").strip().split(" ")
		encode = review_encode(nline)
		encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250) # make the data 250 words long
		predict = model.predict(encode)
		print(line)
		print(encode)
		print(predict[0])