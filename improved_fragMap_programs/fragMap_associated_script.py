import numpy as np
import pandas as pd
from collections import defaultdict
import multiprocessing as mp
import sys
from pathlib import Path
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PIL import Image

def worker(total_rows):
    '''
    Calculates how to split the data
    '''
    
    if total_rows < 10000:
        chunksize = round(total_rows*0.06,0)
    else:
        chunksize = 10000
    
    return chunksize
        
def x_y_z_cols(df_chunk):
    '''
    Creates a two column dataframe with the fragment size and the coorindates it expands
    '''
    
    # Create dataframe with each fragment size associated with each base coorindate it overlaps with
    final = defaultdict(list)
    for indx, row in df_chunk.iterrows():
        if row[9] == row[10]:
            step = 1
        else:
            step = (row[10]-row[9])

        base_frag = np.round(np.linspace(row[9],row[10]-1,step),0)
        frag_size_associated_base_frag = np.repeat([row[6]], len(base_frag))

        final['Coordinate'].extend(base_frag)
        final['Fragment_size'].extend(frag_size_associated_base_frag)

    final_df = pd.DataFrame(final)
    return final_df

def make_matrix(long_df, frag_range, x_array_length):
    '''
    Creates matrix by adding up each repeated coordinate associated with a ceratin fragment size
    '''
    
    lengths = frag_range.split("-")
    
    # Make Fragment_size the row index, Coordinate the col index and Count the values in the matrix
    matrix_unstacked = long_df.set_index(['Fragment_size','Coordinate']).unstack()
    
    # If row indices (y axis) are missing, add them and fill in value with 0. Also, any NaN is filled in with a 0
    matrix_corrected_rows = matrix_unstacked.reindex(list(range(int(lengths[0]),int(lengths[1])+1)),fill_value=0).fillna(0)
    
    # Drop a level of multi index (Count) is order to use the col indexes later on
    matrix_corrected_rows.columns = matrix_corrected_rows.columns.droplevel(0)
    
    # If col indices (x axis) are missing, add them and fill in value with 0
    matrix_corrected_rows_cols = matrix_corrected_rows.reindex(list(range(0,x_array_length)),fill_value=0, axis="columns")

    return matrix_corrected_rows_cols
    
def modifiy_base_per_pixel(table, height, width):
    '''
    Calculates the vertical and horizontal lines per base pair
    '''
    
    # Aspect of height and width
    if height >= 1 and width == 1:
        vertically_repeated = table.reindex(table.index.repeat(height))
        final_matrix = vertically_repeated
        
    elif height >= 1 and width < 1:
        # average first
        # pixels per base
        width_rolling_avg = int(1/width)
        # rolling average and select rows containing the average window HORIZONTALLY
        df_matrix_width_avg = table.rolling(width_rolling_avg, axis=1).mean().dropna(axis=1, how='any')
        avg_matrix = df_matrix_width_avg[df_matrix_width_avg.columns[::width_rolling_avg]]
        # repeat array vertically
        vertically_repeated = avg_matrix.reindex(avg_matrix.index.repeat(height))
        final_matrix = vertically_repeated

    return final_matrix

def plt_image(df_matrix, black_val, frag_range, output_directory, height, width, identifier, region_size, gamma): 
    '''
    Creates an image from a matrix
    '''
    minimum, maximum = frag_range.split("-")
        
    if black_val == "default":
        black_val = int(np.amax(df_matrix))
    else:
        black_val = int(black_val)
        
    plt.rcParams['font.size'] = '9'
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams.update({'font.family':'arial'})
    
    fig, ax = plt.subplots(figsize=(12.6,9.6), dpi=1200)
    im = ax.imshow(df_matrix, vmin=0, vmax=black_val, cmap='binary')
    ax.tick_params(direction='out', length=1.8, width=0.3)

    def conversion_arrayrow(num_list):
        true_yticks = [(i-int(minimum))*int(height) for i in num_list]
        return true_yticks
    
    if int(maximum) - int(minimum) <= 500:
        ylabels = [i for i in range(int(minimum), int(maximum)+1) if i % 50 == 0]
    else:
        ylabels = [i for i in range(int(minimum), int(maximum)+1) if i % 100 == 0]
        
    matrix_length = df_matrix.shape[1] 
    steps = int(matrix_length/10)
    real_xcoor = [i for i in range(0,matrix_length+1, int(steps))] 
    xlabels_ = [i for i in range(int(-matrix_length/2/float(width)),int(matrix_length/2/float(width)+1), int(steps/float(width)))]
    
    if region_size < 10000:
        xlabels = [i if i!=0 else 1 for i in xlabels_]
    else:
        xlabels = [str(int(i/1000))+"k" if i!=0 else 1 for i in xlabels_]
     
    plt.xticks(real_xcoor, xlabels) 
    plt.yticks(conversion_arrayrow(ylabels), ylabels)  
    image_path = Path(output_directory,"_".join([identifier, "fragMap", frag_range,"Max", str(black_val), "X", str(width), "Y", str(height), "Gamma", str(gamma), ".png"]))
    
    ax = fig.gca()
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.2)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.tick_params(which='minor', length=0.8, width=0.3)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(size=1, width=0.3)
    cbar.outline.set_linewidth(0.1)

    plt.savefig(image_path, format='png', facecolor='w', bbox_inches='tight')

    def gammma(x, r):
        """
        From: https://linuxtut.com/en/c3cd5475663c41d9f154/
        Gamma correction y=255*(x/255) 
        x Input image
        r Gamma correction coefficient
        """
        x = np.float64(x)
        y = x/255
        y = y **(1/r)
        
        return np.uint8(255*y)

    if gamma != 1.0:
        img = Image.open(image_path)
        img_gamma = gammma(img, gamma)
        plt.imsave(image_path, img_gamma)
          
    plt.close()
    
if __name__ == '__main__':
    file, rows, black_val, range_frag, output_directory, region_size, height, width, identifier, gamma = sys.argv[1:]
    chunksize = worker(int(rows))

    cols = [6,9,10] # fragment size column = 6, Coor_start column = 9, Coor_end column = 10
    reader = pd.read_csv(file, sep="\t", header=None, chunksize=chunksize, iterator=True,  dtype={6:int, 9:int, 10:int})
    
    pool = mp.Pool(mp.cpu_count())
    hist_cols_df = pool.map(x_y_z_cols, [read for read in reader])
    pool.close()
    df_to_graph = pd.concat(hist_cols_df).groupby(by=['Fragment_size','Coordinate']).size().reset_index().rename(columns = {0:'Count'})
    big_df = make_matrix(df_to_graph, range_frag, int(region_size))

    if float(height) == 1.0 and float(width) == 1.0:
        plt_image(big_df.to_numpy(), black_val, range_frag, output_directory, float(height), float(width), identifier, int(region_size), float(gamma))

    else:
        avg_df = modifiy_base_per_pixel(big_df, float(height), float(width))
        # matplotlib input is numpy array
        plt_image(avg_df.to_numpy(), black_val, range_frag, output_directory, float(height), float(width), identifier, int(region_size), float(gamma))
