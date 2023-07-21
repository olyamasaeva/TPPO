from numpy import*
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


filename = 'acc_00001.csv'
df = pd.read_csv(filename, header=None)

signal = df[4].values               
(cA1,  cD1)  =  pywt .dwt (signal,  'db2', 'smooth')
signal

wavelet = 'cmor1-0.5' 
ax = scg.cws(signal, scales=arange(1, 40), wavelet=wavelet, figsize=(8, 4), cmap="jet", cbar=None, ylabel='Период ',yscale="log", xlabel="Время ",
title='Вейвлет-преобразование сигнала  %s \n(спектр мощности)'%filename)
show()