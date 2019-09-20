from sklearn.neighbors import KNeighborsClassifier
import numpy as np



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
            y.append(labels[i,t,:])
    cls = KNeighborsClassifier(n_neighbors=5)
    cls.fit(X, y)
    return cls

def do_prediction(input_embedding, labels, target_embedding):
    print("Training classifier")
    cls = get_knn_classifier(input_embedding, np.rot90(labels,3))
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
    predicted = cls.predict(predict_on)
    print("finished classifying")

    done = 0
    for i in range(mx):
        for t in range(my):
            result[i, t, :] = predicted[done]
            done += 1
    
    return result

    