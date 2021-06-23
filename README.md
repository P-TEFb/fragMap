# fragMap
Creates heatmaps displaying the total number of fragments across genomic positions of a given interval or a list of intervals.

Author: Mrutyunjaya Parida, David Price lab, UIOWA

## Usage:
ABD runs on Python 2.7+ interpreter installed on your desired operating system of choice such as Windows, Mac or Linux. 

ABD program needs 4 mandatory parameters to run as described below.
```
python ABD <mapped-fragments.bed> <genome-sequence.fa> <output-file-prefix> <number-of-cores>

Example run: python ABD Sample1.deduped.bed /home/xyz-user/genomes/hg38.genome.fa Pol-II 20
```
