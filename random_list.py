import os
import numpy as np

class RandomList():
    def __init__(self, N):
        self.N = N
        self.indices = np.arange(N)

    def step(self):
        idx = np.random.randint(0, len(self.indices))
        index = self.indices[idx]
        self.indices = np.delete(self.indices, idx)
        if len(self.indices) == 0:
            self.indices = np.arange(self.N)
        return index

if __name__ == '__main__':
    N = 5
    r = RandomList(N)
    while 1:
        print(r.step())
