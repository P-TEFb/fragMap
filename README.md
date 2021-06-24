# fragMap
Creates heatmaps displaying the total number of fragments of each fragment size across intervals of a specific size.

Author: Mrutyunjaya Parida, David Price lab, UIOWA

## Usage:
fragMap pipeline runs on Python 2.7+ interpreter and R 3.6.3v installed on your desired operating system of choice such as Windows, Mac or Linux. 

First, the fragMap-table program make a data table in .csv format containing total pile-up of a fragmentsize for each basepair across intervals using the following parameters as described below.
```
python fragMap-table <genomic-intervals.bed> <mapped-fragments.bed> <number of genomic intervals>

Example run: python fragMap-table intervals.bed Sample1.bed 25000
```
Second, the fragMap-tick program duplicates the rows and columns of the fragMap data table as per the user's preference to maintain a certain height, width, and aspect ratio of the final image. Additionally, the fragMap-tick program adds major and minor tickmarks of a specific size on the bottom and right side of the fragMap data table. The following parameters are used to run this program.
```
python fragMap-tick <mapped-fragments.datatable.csv> <fragMap height> <fragMap width> <tick size> <mapped-fragments.datatable.max>

Example run: python fragMap-tick Sample1.datatable.csv 4 1 10 Sample1.datatable.max   
```
