import pandas as pd
import numpy as np
import subprocess
import sys
from pathlib import Path
import argparse

def run_bedtools(regions, reads):
    '''
    Checks that all regions in the file are of the same length and that they 
    match the chosen fragmap type before running bedtools.    
    '''
    
    # Check if every region has the same size
    dff = pd.read_csv(regions, sep="\t", header=None)
    dff['region_size'] = dff[2] - dff[1]
    if len(dff['region_size'].unique()) != 1:
        print("Regions are not all of the same length")
        sys.exit()

    temp_data_bedtools = Path(Path.cwd(),'bedtools_output.bed')
    subprocess.call(' '.join(['bedtools intersect -a', regions, '-b', reads, '-wa', '-wb', '>', str(temp_data_bedtools)]), shell=True)
    
    return temp_data_bedtools

def main(data_file,frags_filtering, max_val, output_directory, height, width, identifier):
    '''
    Gets bedtools output by uploading only a slected number of columns.
    Calculates fragment sizes, selected them based on fragmap type and calucaltes coordinates of the fragments by strandeness of regions.
    Runs the second program associated with fragmap.py    
    '''
    
    cols = [1,2,5,7,8,11]
    df_bedtools = pd.read_csv(data_file, sep="\t", header=None, usecols=cols)
        
    # Region size
    region_size = df_bedtools[2][0] - df_bedtools[1][0]
    
    # Fragment size col
    df_bedtools['Fragment_size'] = df_bedtools[8] - df_bedtools[7]
    
    # Convert intervals where one or both of the sides are smaller or larger than the region into the region limits 
    df_bedtools['New_read_start'] = np.where(df_bedtools[7] < df_bedtools[1], df_bedtools[1], df_bedtools[7])
    df_bedtools['New_read_end'] = np.where(df_bedtools[8] > df_bedtools[2], df_bedtools[2], df_bedtools[8])
    
    # Convert coordinate to distance from Start_region
    df_bedtools['Coor_start'] = np.where(df_bedtools[5]=='+', (df_bedtools["New_read_start"] - df_bedtools[1]), df_bedtools[2] - df_bedtools["New_read_end"])
    df_bedtools['Coor_end'] = np.where(df_bedtools[5]=='+', (df_bedtools["New_read_end"] - df_bedtools[1]), df_bedtools[2] - df_bedtools["New_read_start"])
    
    # Only use rows where the start of the read is not the last coordinate of the region
    df_bedtools = df_bedtools[df_bedtools['Coor_start'] < region_size]
    
    # Calculate total rows 
    total_rows = df_bedtools.shape[0]
    
    # Select fragment sizes
    lengths = frags_filtering.split("-")
    size_left = int(lengths[0]) # inlcusive
    size_right = int(lengths[1]) # NOT inclusive

    if size_left > size_right:
        print("Fragment size range is incorrect")
        sys.exit()            

    df_bedtools = df_bedtools.loc[(df_bedtools['Fragment_size'] >= size_left) & (df_bedtools['Fragment_size'] < size_right)].reset_index(drop=True)
    
    temp_data = Path(Path.cwd(),'data.bed')
    df_bedtools.to_csv(temp_data, sep="\t", index=False, header=False)
    
    subprocess.run(['python3', 'fragMap_associated_script.py', temp_data, str(total_rows), str(max_val), str(fragment_sizes), output_directory, str(region_size), str(height), str(width), identifier])

    temp_data.unlink()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='fragMap.py',
                                     description='Generates a fragMap from specific range of fragment sizes over a chosen genomic interval')
    parser.add_argument('regions', type=str,
                        help='Bed file of genomic regions of chosen length')
    parser.add_argument('fragments', type=str,
                        help='Bed file of fragment positions')
    parser.add_argument('-r', dest="range", metavar='\b', type=int, nargs=2,
                        help='Range of fragment sizes, for exmaple -r 20 400')
    parser.add_argument('-b', dest="black", metavar='\b', default='default',
                        help='Sets the chosen value as black, default is largest number in the matrix')
    parser.add_argument('-y', dest="y_axis", metavar='\b', type=int, default=1,
                        help='Horizontal lines/bp for each fragment length')
    parser.add_argument('-x', dest="x_axis", metavar='\b', type=float, default=1.0,
                        help='Vertical lines/bp for each genomic interval displayed, for example -x 1 is one vertical line/bp; -x 0.1 is one vertical line/10 bp')
    parser.add_argument('-o', dest="output_dir", metavar='\b', type=str, required=True, nargs=2,
                        help='Image identifier and path to output, for example -o TBP /home/user/dir')

    args = parser.parse_args()
    
    file = args.regions
    read_file = args.fragments
    fragment_sizes = args.range
    max_val = args.black
    height = args.y_axis
    width = args.x_axis
    output_directory, identifier = args.output_dir

    if len(sys.argv[1:]) != 3:
        sys.argv.append('--help')
    try:
        fragment_sizes = str(fragment_sizes[0])+"-"+str(fragment_sizes[1])
    except (TypeError, AttributeError, ValueError):
        print('Missing range argument. Fragment size range example: -r 20 400')
        sys.exit()
    try:
        int(height)
    except (TypeError, AttributeError, ValueError):
        print("Missing -y argument. y must be int")
        sys.exit()
    try:
        float(width) or int(width)
    except (TypeError, AttributeError, ValueError):
        print("Missing -x argument. x must be int or float")
        sys.exit()

    if max_val != 'default':
        try:
            int(max_val) or float(max_val)
        except (TypeError, AttributeError, ValueError):
            print("black value: int or default")
            sys.exit() 
    
    bedtools_file_path = run_bedtools(file, read_file)    
    main(bedtools_file_path, fragment_sizes, max_val, output_directory, height, width, identifier)
    # delete temp file
    bedtools_file_path.unlink()
