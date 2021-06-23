# fragMap
Creates heatmaps displaying the total number of fragments across genomic positions of a given interval or a list of intervals.

Author: Mrutyunjaya Parida, David Price lab, UIOWA

## Usage:
fragMap pipeline runs on Python 2.7+ interpreter and R 3.6.3v installed on your desired operating system of choice such as Windows, Mac or Linux. 

fragMap-table program needs the following mandatory parameters to run as described below.
```
python fragMap-table <genomic-intervals.bed> <mapped-fragments.bed> <number of genomic intervals>

Example run: python fragMap-table intervals.bed Sample1.bed 25000
```
