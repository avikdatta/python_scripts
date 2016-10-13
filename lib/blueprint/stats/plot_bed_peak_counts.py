#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def plot_box_chart(dataframe, filename,chr_list, fig_width=12, fig_height=8, fig_font=10, title='Peak count Boxplot'):
  '''
  Plot dataframe as boxplot using Matplotlib
  '''
  plt.figure(figsize=(fig_width,fig_height))
  plt.autoscale(enable=True)
  plt.title(title)
  dataframe[chr_list].boxplot(fontsize=fig_font,return_type='dict')
  plt.savefig(filename,bbox_inches='tight')
  plt.close("all")


def groupby_histone(dataframe,histone):
  '''
  Get experiments for a specific histone mark as a list
  '''
  histone_exps=dataframe.groupby('EXPERIMENT_TYPE').get_group(histone).groupby('EXPERIMENT_ID').groups.keys()
  return list(histone_exps)

