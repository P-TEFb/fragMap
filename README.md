# fragMap
Creates heatmaps displaying the total number of fragments of each fragment size across intervals of a specific size.

Author: Mrutyunjaya Parida, David Price lab, UIOWA

## Usage:
fragMap pipeline runs on Python 2.7+ interpreter and R 3.6.3v installed on your desired operating system of choice such as Windows, Mac or Linux. 

First, the fragMap-table program make a data table containing count of each fragmentsize for each basepair across intervals using the following parameters as described below.
```
python fragMap-table <genomic-intervals.bed> <mapped-fragments.bed> <number of genomic intervals>

Example run: python fragMap-table intervals.bed Sample1.bed 25000
```
