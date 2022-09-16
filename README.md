# fragMap.py #
Juan F. Santana, Ph.D. (<juan-santana@uiowa.edu>), University of Iowa, Iowa City, I.A.

David H. Price, Ph.D. (<david-price@uiowa.edu>), University of Iowa, Iowa City, I.A.

This script runs on Python 3+ in Linux operating system. It will create fragment heatmaps from specific range of fragment sizes over a chosen genomic interval as described here [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) and here [Santana et al., 2022](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkac678/6659871?guestAccessKey=88024805-7d8e-4421-a032-dbef1c737757). 

# File requirements #
The input regions file should be a six column tab delimited bed file that contains chromosome, start and end positions as well as the strand information for each region.  
 
| chr6 | 142946246 | 142946446 | Gene_A | 255 | - |
|:----:|:---------:|:---------:|:------:|:---:|:-:|

The input fragments file should be a six column tab delimited bed file that contains chromosome, start and end positions as well as the strand information for each fragment.

| chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
Generates a fragMap from specific range of fragment sizes over a chosen genomic interval. 

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

Matplotlib: https://matplotlib.org/stable/users/installing/index.html

### Program used to obtain the fragments overlapping the genomic intervals ###
bedtools: https://bedtools.readthedocs.io/en/latest/content/installation.html, developed by the Quinlan laboratory at the University of Utah. 

# Example of arguments #
```
python fragMap.py <regions> \
                  <fragments> \
                  <fragment_type> \
                  -r \
                  -b \
                  -y \
                  -x \
                  -o \


Example command usage: 
python fragMap.py plusminus1000_from_TSS_1000genes.bed \
                  TBP-DFF-ChIP-Seq.bed \
                  -o TBP /home/user/dir \
                  -r 20 1000 \
                  -x 0.1 \

```
# Parameter description #
### Required arguments ###
```
regions: <str> Bed file of genomic regions of chosen length.

fragments: <str> Bed file of fragment positions

-o: <str> <str> Image identifier and path to output, for example -o TBP /home/user/dir

-r: <int> <int> Range of fragment sizes, for exmaple -r 20 400
```
### Optional arguments ###
```
-b: <int> Sets the chosen value as black, default is largest number in the matrix

-y: <int> (value greater or equal to 1) Horizontal lines/bp for each fragment length, default is 1

-x: <float> (value less or equal to 1) Vertical lines/bp for each genomic interval displayed, for example -x 1 is one vertical line/bp; -x 0.1 is one vertical line/10 bp, default is 1

```
