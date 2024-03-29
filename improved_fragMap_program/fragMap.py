import pandas as pd
import numpy as np
import subprocess
import sys
from pathlib import Path
import argparse
try:
    import fragMap_associated_script
except (ImportError, ModuleNotFoundError):
    sys.exit("fragMap_associated_script.py was not imported correctly. Make sure that it is in the same directory as fragMap.py")

def run_bedtools(regions, reads):
    '''
    Checks that all regions in the file are of the same length before running bedtools.    
    '''
    
    # Check if every region has the same size
    dff = pd.read_csv(regions, sep="\t", header=None)
    dff['region_size'] = dff[2] - dff[1]
    
    if len(dff['region_size'].unique()) != 1:
        sys.exit("Regions are not all of the same length")

    subprocess.call(' '.join(['bedtools intersect -a', regions, '-b', reads, '-wa', '-wb', '>', str(temp_data_bedtools)]), shell=True)
    
    return temp_data_bedtools

def main(data_file, max_val, output_directory, height, width, identifier, gamma, size_left, size_right):
    '''
    Gets bedtools output by uploading only a selected number of columns.
    Calculates fragment sizes, calculates coordinates of the fragments by strandeness of regions.
    Runs the second program associated with fragmap.py    
    '''
    
    cols = [1,2,5,7,8,11]
    df_bedtools = pd.read_csv(data_file, sep="\t", header=None, usecols=cols)
        
    # Region size
    region_size = df_bedtools[2][0] - df_bedtools[1][0]
    
    # Fragment size col
    df_bedtools['Fragment_size'] = (df_bedtools[8] - df_bedtools[7]) + 1
    
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
    
    # Filter by fragment size
    df_bedtools = df_bedtools.loc[(df_bedtools['Fragment_size'] >= size_left) & (df_bedtools['Fragment_size'] <= size_right)].reset_index(drop=True)
    
    # Create tmp file
    df_bedtools.to_csv(temp_data, sep="\t", index=False, header=False)
    
    return total_rows, region_size

def parse_args():
    '''
    Get arguments and make multiple checks
    '''
    
    parser = argparse.ArgumentParser(prog='fragMap.py',
                                     description='Generates a fragMap from specific range of fragment sizes over a chosen genomic interval')
    parser.add_argument('regions', type=str,
                        help='Bed file of genomic regions of chosen length')
    parser.add_argument('fragments', type=str,
                        help='Bed file of fragment positions')
    parser.add_argument('-r', dest="range", metavar='\b', type=int, nargs=2, required=True,
                        help='Range of fragment sizes, for exmaple -r 20 400')
    parser.add_argument('-b', dest="black", metavar='\b', default='default',
                        help='Sets the chosen value as black, default is largest number in the matrix')
    parser.add_argument('-y', dest="y_axis", metavar='\b', type=int, default=1,
                        help='Horizontal lines/bp for each fragment length')
    parser.add_argument('-x', dest="x_axis", metavar='\b', type=float, default=1.0,
                        help='Vertical lines/bp for each genomic interval displayed, for example -x 1 is one vertical line/bp; -x 0.1 is one vertical line/10 bp')
    parser.add_argument('-g', dest="gamma", metavar='\b', type=float, default=1.0,
                        help='Gamma correction')
    parser.add_argument('-o', dest="output_dir", metavar='\b', type=str, required=True, nargs=2,
                        help='Image identifier and path to output, for example -o TBP /home/user/dir')

    args = parser.parse_args()
    
    file = args.regions
    read_file = args.fragments
    fragment_sizes = args.range
    max_val = args.black
    height = args.y_axis
    width = args.x_axis
    gamma = args.gamma
    identifier, output_directory = args.output_dir
    
    if len(sys.argv[1:]) != 4:
        sys.argv.append('--help')
    try:
        fragment_sizes = str(fragment_sizes[0])+"-"+str(fragment_sizes[1])
    except (TypeError, AttributeError, ValueError):
        sys.exit('Missing range argument. Fragment size range example: -r 20 400')
    if float(width) > 1:
        sys.exit("Missing -x argument. x must be int or float less than or equal to 1")
    if max_val != 'default':
        try:
            int(max_val) or float(max_val)
        except (TypeError, AttributeError, ValueError):
            sys.exit("black value: int or default") 
            
    # Fragment sizes
    size_left, size_right = args.range # inlcusive

    if size_left > size_right:
        sys.exit("Fragment size range is incorrect")         
            
    return file, read_file, fragment_sizes, max_val, height, width, gamma, output_directory, identifier, size_left, size_right
    
if __name__ == '__main__':
    file, read_file, fragment_sizes, max_val, height, width, gamma, output_directory, identifier, size_left, size_right = parse_args()
    
    temp_data_bedtools = Path(Path.cwd(),'bedtools_output.bed')
    bedtools_file_path = run_bedtools(file, read_file) 
    
    temp_data = Path(Path.cwd(),'data.bed')
    total_rows, region_size = main(bedtools_file_path, max_val, output_directory, height, width, identifier, gamma, size_left, size_right)
        
    # Run the associated script on the filtered data
    fragMap_associated_script.main(temp_data,
                                   total_rows,
                                   max_val,
                                   fragment_sizes,
                                   output_directory,
                                   region_size,
                                   height,
                                   width,
                                   identifier,
                                   gamma)

    # delete temp files
    bedtools_file_path.unlink()
    temp_data.unlink()
