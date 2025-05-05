import numpy as np
import matplotlib.pyplot as plt
from pprint import pp

test_list = [[i for t in range(10)] for i in range(3)]
pp(test_list)
np_list = np.array(test_list)
pp(np_list)
pp(np_list.shape)
mean_list = np.mean(np_list, axis=0)
pp(mean_list)
pp(mean_list.shape)
std_list = np.std(np_list, axis=0)
pp(std_list)
pp(std_list.shape)
