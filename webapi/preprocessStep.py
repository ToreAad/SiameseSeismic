from tensorflow.keras.models import load_model
import segyio
import numpy as np

print("Loading seismic")
f3 = segyio.tools.cube("./data/F3_entire.segy")
print(f3.shape)
input_slice = f3[200:216, :512, :512]
target_slice = f3[-216:-200, :512, :512]

# import matplotlib.pyplot as plt

# plt.imshow(input_slice[0,:,:])
# plt.show()
# plt.imshow(target_slice[0,:,:])
# plt.show()

print(input_slice.shape)
print(target_slice.shape)

np.save("input_slice.npy", input_slice)
np.save("target_slice.npy", target_slice)

model = load_model("./mlModels/trainedSiameseNetwork.h5")

(mx, mi, mt) = input_slice.shape

mi_em = mi-16-mi%16
mt_em = mt-16-mt%16
print(mi_em, mt_em)
input_embedding = np.zeros((64, mi_em, mt_em))
target_embedding = np.zeros((64, mi_em, mt_em))

done = 0
total = (mi_em)*(mt_em)

input_to_predict = []
target_to_predict = []

for i in range(mi_em):
    for t in range(mt_em):
        if done%500 == 0:
            print("Done {}% of total, doing slice {}->{}, {}->{}".format(100*(done/total), i, i+16, t, t+16))
        input_window = input_slice[0:16,i:i+16,t:t+16].reshape((16,16,16))
        target_window = target_slice[0:16,i:i+16,t:t+16].reshape((16,16,16))
        input_to_predict.append(input_window)
        target_to_predict.append(target_window)
        done += 1

done = 0
predicted_input = model.predict( np.array(input_to_predict))
predicted_target = model.predict( np.array(target_to_predict))
print(predicted_input.shape)
for i in range(mi_em):
    for t in range(mt_em):
        if done%500 == 0:
            print("Done {}% of total, doing slice {}->{}, {}->{}".format(100*(done/total), i, i+16, t, t+16))
        input_embedding[:,i,t] = predicted_input[done]
        target_embedding[:,i,t] = predicted_target[done]
        done += 1


#print(predicted_input.shape)

np.save("input_embedding.npy", input_embedding)
np.save("target_embedding.npy", target_embedding)

