import os
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import pywt
from scipy import *
import pandas as pd
from pylab import *
import scaleogram as scg
from sklearn.cluster import KMeans
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
import sys
from sys import exit
import os

def lowpassfilter(signal, thresh, wavelet='bior4.4', mode='soft'):
    thresh = thresh * nanmax(signal)
    coeff = pywt.wavedec(signal, wavelet, level=8, mode="per")
    coeff[1:] = (pywt.threshold(i, value=thresh, mode=mode)
                 for i in coeff[1:])
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
    return reconstructed_signal

def generate_plots(signal, destdir, src_filename):
    # wavelet-cmor
    print('Выполнение Вейвлет-преобразования...')
    wavelet = 'cmor1-0.5'
    wavelet_cmor_fig, wavelet_cmor_ax = plt.subplots(1, 1)
    scg.cws(signal, scales=arange(1, 40), wavelet=wavelet, coikw={'alpha': 0.5, 'hatch': '/'},
            cmap="jet", cbar=None, ylabel='Период ', yscale="log", xlabel="Время ", ax=wavelet_cmor_ax)
    wavelet_cmor_fig.savefig(destdir + os.sep + 'wavelet_cmor.png')

    # wavelet-bior
    print('Очистка сигнала Вейвлет-преобразованием...')
    mode = 'soft'
    v = 'bior4.4'
    wavelet_bior_fig, wavelet_bior_ax = plt.subplots()
    wavelet_bior_ax.plot(signal, color="b", alpha=0.5, label='Оригинальный сигнал')
    rec = lowpassfilter(signal, 0.4, mode=mode)
    wavelet_bior_ax.plot(rec, 'r', label='DWT преобразование сигнала', linewidth=2)
    wavelet_bior_ax.legend()
    wavelet_bior_ax.set_ylabel('Амплитуда сигнала', fontsize=10)
    wavelet_bior_ax.set_xlabel('Время', fontsize=10)
    wavelet_bior_fig.savefig(destdir + os.sep + 'wavelet_bior.png')

    # wavelet_cleaned
    print('Выполнение Вейвлет-преобразования очищенного сигнала...')
    wavelet_cleaned_fig, wavelet_cleaned_ax = plt.subplots(1, 1)
    wavelet_cleaned_ax.set_xlabel('Время')
    wavelet_cleaned_ax.set_ylabel('Период')
    wavelet_cleaned_ax.set_yscale('log')
    scg.cws(rec, scales=arange(1, 40), wavelet=wavelet, ax=wavelet_cleaned_ax,
        coikw={'alpha': 0.5, 'hatch': '/'}, cmap="jet", cbar=None, ylabel='Период', yscale="log", xlabel="Время")
    wavelet_cleaned_fig.savefig(destdir + os.sep + 'wavelet_cleaned.png')

    # cleaned
    cleaned_fig, cleaned_ax = plt.subplots(1, 1)
    cleaned_ax.plot(rec, color="b", alpha=0.5, label='Обработанный сигнал')
    cleaned_fig.savefig(destdir + os.sep + 'cleaned.png')

    hist_fig, hist_ax = plt.subplots(1, 1)
    hist_ax.hist(rec, bins=100) 
    hist_fig.savefig(destdir + os.sep + 'histogram.png')