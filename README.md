# fragMap
Creates heatmaps displaying the total number of fragments of each fragment size across intervals of a specific size.

Author: Mrutyunjaya Parida, David Price lab, UIOWA

## Usage:
fragMap pipeline runs on Python 2.7+ interpreter and R 3.6.3v installed on your desired operating system of choice such as Windows, Mac or Linux. 

First, the fragMap-table program make a data table in .csv format containing total number of mapped fragments of a specific size for each basepair across intervals using the following parameters as described below.
```
python FRAGMAP-TABLE.py <genomic-intervals.bed> <mapped-fragments.bed> <number of genomic intervals>

Example run: python FRAGMAP-TABLE.py intervals.bed Sample1.bed 25000
```

Second, the fragMap-tick program duplicates the rows and columns of the fragMap data table as per the user's preference to maintain a certain height, width, and aspect ratio of the final image. Additionally, the fragMap-tick program adds major and minor tickmarks of a specific size on the bottom and right side of the fragMap data table. The following parameters are used to run this program.
```
python TICKMARKS-3px-GENOMICINTERVALS.py <mapped-fragments.data-table.csv> <fragMap height> <fragMap width> <tick length> <lightness>

Example run: python fragMap-tick Sample1.data-table.csv 4 1 10 Sample1.data-table-lightness.txt   
```

Third, the R script makes the fragMap image from the fragMap data table. The following parameters are used to run this program.
```
Rscript FMAP.R <mapped-fragments.data-table.csv> <mapped-fragments.data-table.max>

Example run: Rscript FMAP.R Sample1.data-table.csv Sample1.data-table.max   
```
