# fragMap.py #
Juan F. Santana, Ph.D. (<juan-santana@uiowa.edu>), University of Iowa, Iowa City, I.A.

David H. Price, Ph.D. (<david-price@uiowa.edu>), University of Iowa, Iowa City, I.A.

The fragMap program (split into two python files: fragMap.py and fragMap_associated_script.py - please maintain both files in the same directory) runs on Python 3+ in Linux operating system (due to the use of the bedtools program discussed below). It will create fragment heatmaps from specific range of fragment sizes over a chosen genomic interval as described in [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) and [Santana et al., 2022](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkac678/6659871?guestAccessKey=88024805-7d8e-4421-a032-dbef1c737757). 

# File requirements #
The input regions file should be a six column tab delimited bed file that contains chromosome, start and end positions as well as the strand information for each region. The regions can be of any length as long as the length is an even number and the center is a feature under study (e.g. transcription start site (TSS)). 
 
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
python3 fragMap.py <regions> \
                  <fragments> \
                  -r \
                  -b \
                  -y \
                  -x \
                  -g \
                  -o \


Example command usage: 
python3 fragMap.py plusminus1000_from_TSS_1000genes.bed \
                  PolII-DFF-ChIP-Seq.bed \
                  -o PolII /home/user/dir \
                  -r 20 400 \
                  -y 4 \
                  -g 0.5

```
# Parameter description #
### Required arguments ###
```
regions: <str> Bed file of genomic regions of chosen length with the format described above

fragments: <str> Bed file of fragment positions with the format described above

-o: <str> <str> Image identifier and path to output directory, for example -o TBP /home/user/dir

-r: <int> <int> Range of fragment sizes, for example -r 20 400
```
### Optional arguments ###
```
-b: <int> Sets the chosen value as black, default is largest number in the matrix

-y: <int> (value greater than or equal to 1) Horizontal lines/bp for each fragment length, default is 1

-x: <float> or <int> (value less than or equal to 1) Vertical lines/bp for each genomic interval displayed, for example -x 1 is one vertical line/bp; -x 0.1 is one vertical line/averaged 10 bp, default is 1

-g: <float> Gamma correction factor, default is 1 (for more information: https://en.wikipedia.org/wiki/Gamma_correction)

```
Example output from Pol II DFF-Seq performed on HFF cells ([Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x)) over +/- 1,000 bp regions from the MaxTSS of 12,229 genes in HFF cells determined with PRO-Cap ([Nilson et al., 2022](https://doi.org/10.1093/nar/gkac678)): 

PolII_fragMap_20-400_Max_68609_X_1 0_Y_4_Gamma_1.0 
![PolII_fragMap_Custom_20-400_Max_68609_X_1 0_Y_4 0_](https://user-images.githubusercontent.com/38702786/190675335-1b8271ef-a0f7-449e-9ac3-aeee7dca6611.png)
