from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import random



def get_knn_classifier(embedding_array, label_array):
    (_, mx, my) = embedding_array.shape
    (mx_, my_, _) = label_array.shape
    mx = min(mx_, mx)
    my = min(my_, my)
    labels = label_array[:mx, :my, :]

    X = []
    y = []
    for i in range(mx):
        for t in range(my):
            X.append(embedding_array[:,i, t])
            r,g,b,a = labels[i,t,:]
            y.append((r,g,b,a))
    encode = dict((key, val) for val, key in enumerate(set(y)))
    decode = dict((key, val) for val, key in encode.items())
    y_ = [encode[v] for v in y]
    clf = RandomForestClassifier()
    print("Fitting classifier")
    selection = random.sample(list(range(len(X))), 5000)
    clf.fit([X[i] for i in selection], [y_[i] for i in selection])
    return clf, decode

def do_prediction(input_embedding, labels, target_embedding):
    print("Training classifier")
    clf, decode = get_knn_classifier(input_embedding, np.rot90(labels,3))
    print("Finished training classifier")

    (_, mx, my) = target_embedding.shape
    result = np.zeros((mx,my, 4))

    predict_on = []
    done = 0
    for i in range(mx):
        for t in range(my):
            done += 1
            predict_on.append(target_embedding[:,i,t])

    print("Running classifier")
    predicted = clf.predict(predict_on)
    print("finished classifying")

    done = 0
    for i in range(mx):
        for t in range(my):
            prediction = predicted[done]
            (r,g,b,a) = decode[prediction]
            result[i, t, :] = np.array([r,g,b,a])
            done += 1

    return result
