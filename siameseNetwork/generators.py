import numpy as np
import bruges as bg
import segyio
import random
import os
from tensorflow.keras.utils import Sequence

def read_odt_pts(fname):
    data = np.loadtxt(fname, skiprows=6, comments='!', usecols=[0,1,2])
    return data


def pts_to_ixt(fname, dt=0.004):
    f3_corners_xy = np.array([
    [605835.5, 6073556.3],
    [629576.3, 6074219.9],
    [629122.5, 6090463.2]
    ])

    f3_corners_ix = np.array([[0,  0],
                        [0, 950],
                        [650, 950]
                        ])
    data = read_odt_pts(fname)
    transform = bg.transform.CoordTransform(f3_corners_ix, f3_corners_xy)
    ix = [transform.reverse(r) for r in data[:, :2]]
    t = (data[:, 2][:, None] / dt).astype(int)
    ixt = np.hstack([ix, t])
    return ixt

print("Loading seismic")
f3 = segyio.tools.cube("./data/F3_entire.segy")
print("Seismic loaded")

class Singlet(Sequence):
    def __init__(self, batch_size, directory, steps_per_epoch, shape=(3,48,48)):
        self.batch_size = batch_size
        self.directory = directory
        self.steps_per_epoch = steps_per_epoch
        self.classes = os.listdir(directory)
        self.coos = []
        for label in self.classes:
            print(label)
            label_coos = pts_to_ixt(os.path.join(self.directory, label))
            self.coos.append(label_coos)
        self._shape = shape
        self.n_classes = len(self.classes)

    def __len__(self):
        return self.steps_per_epoch

    def get_image(self, label_id, coo_id):
        (i, x, t) = self.coos[label_id][coo_id]
        (di, dx, dt) = self._shape
    
        (mx_i, mx_x, mx_t) = f3.shape
        i = min(i, mx_i-di)
        x = min(x, mx_x-dx)
        t = min(t, mx_t-dt)
        im = f3[i:i+di, x:x+dx, t:t+dt]
        return im

    def __getitem__(self, idx):
        images = np.ones((self.batch_size, *self._shape))
        labels = []
        for blank_img in images:
            label_id = random.randint(0, len(self.classes)-1)
            coo_id = random.randint(0, len(self.coos[label_id])-1)
            labels.append(label_id)
            blank_img[:,:,:] = self.get_image(label_id, coo_id)
        return (np.asarray(images), np.asarray(labels))

class Triplet(Singlet):
    def __getitem__(self, idx):
        a_img = np.ones((self.batch_size, *self._shape))
        p_img = np.ones((self.batch_size, *self._shape))
        n_img = np.ones((self.batch_size, *self._shape))
        labels = []
        for j in range(self.batch_size):
            pos_class = random.randint(0, len(self.classes)-1)
            neg_class = random.randint(0, len(self.classes)-2)
            if neg_class >= pos_class:
                neg_class = neg_class + 1

            a_random_choice = random.randint(0, len(self.coos[pos_class])-1)
            p_random_choice = random.randint(0, len(self.coos[pos_class])-1)
            n_random_choice = random.randint(0, len(self.coos[neg_class])-1)

            a_img[j,:,:,:] = self.get_image(pos_class, a_random_choice)
            p_img[j,:,:,:] = self.get_image(pos_class, p_random_choice)
            n_img[j,:,:,:] = self.get_image(neg_class, n_random_choice)
            labels.append((pos_class, neg_class))

        return([a_img, p_img, n_img], np.asarray(labels))

# Testing:
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    base_batch_size = 4
    train_dir = "./data/pointDatasets/"
    shape = (32,32, 32)
    steps_per_epoch = 16
    print("### Testing Singlet generator class ###")
    train_generator = Singlet(
        batch_size=base_batch_size, directory=train_dir, steps_per_epoch=steps_per_epoch, shape = shape)
    for i in range(1):
        image, label = train_generator[i]
        for j in image:
            plt.imshow(np.rot90(j[0, :, :]), cmap="seismic")
            plt.show()

    print("### Testing Triplet generator class ###")
    train_generator = Triplet(
        batch_size=base_batch_size, directory=train_dir, steps_per_epoch=steps_per_epoch, shape = shape)
    for i in range(1):
        [a_imgs, p_imgs, n_imgs], y = train_generator[i]
        for j in a_imgs:
            plt.imshow(np.rot90(j[0, :, :]), cmap="seismic")
            plt.show()