import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pandas as pd
from IPython import embed

def load_gt():
    with open('data/catalog12g7l.txt', 'r') as f:
        gt_txt = f.read()
        gt_lines = gt_txt.strip().split('\n')[1:]
        gt_lines = list(map(lambda x: x.split(' '), gt_lines))
        gt_arr = np.array(list(map(lambda x: list(map(float, x)), gt_lines)))
        x_gt, score_gt = gt_arr[:, 0], gt_arr[:, 1]
    return x_gt, score_gt
    
def plot_pred(data, x_gt, test_scores):
    plt.figure(figsize=(16, 8))
    plt.imshow(data, aspect='auto', vmin=-4e-4, vmax=4e-4, extent=[0, 3600, 1250, 0], cmap=plt.cm.RdYlBu)
    for x in x_gt:
        #plt.axvspan(x, color='red', alpha=1)
        plt.axvline(x)
    plt.xlabel('Time [s]')
    plt.ylabel('Station Number')
    plt.colorbar()
    plt.savefig('images/gt.pdf')
    plt.close()
    # embed()
    
    pred_mean = test_scores[20:].mean(0)

    for q in np.arange(0.97, 1, 0.001):
        plt.figure(figsize=(16, 8))
        plt.imshow(data, aspect='auto', vmin=-4e-4, vmax=4e-4, extent=[0, 3600, 1250, 0], cmap=plt.cm.RdYlBu)

        f = open('images/q_{}.txt'.format(q), 'w')
        q_value = np.quantile(pred_mean, q)
        for i in range(pred_mean.size):
            if pred_mean[i] > q_value:
                x_plot = i/25 + 2000
                # plt.axvspan(i/25 + 2000, i/25 + 2000 + 1, color='red', alpha=0.5)
                plt.axvline(i/25 + 2000, color='red', linewidth=0.5, ymin=0.2, ymax=0.8)
                f.write(str(i+50000)+'\n')

        for x in x_gt:
            plt.axvline(x, color='blue', linewidth=0.5)

        f.close()

        plt.xlabel('Time [s]')
        plt.ylabel('Station Number')
        plt.colorbar()
        plt.savefig('images/q_{}.pdf'.format(q))
        print('images/q_{}.pdf'.format(q))

