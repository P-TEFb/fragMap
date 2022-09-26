# fragMap-original
Original fragMap program Documentation. 
Author: Mrutyunjaya “Rocky” Parida, and David Price.

The fragMap program runs via a Python v2.7+ interpreter installed on your desired operating system of choice such as Windows, Mac or Linux. Here is the link to download the program: https://drive.google.com/file/d/1cPIhkDtagXnBZY1jP7DNyDltoLr8vjmM/view?usp=sharing.

First, the FRAGMAP-TABLE program makes a data table containing total number of mapped fragments for a range of fragment sizes and a set of equal size genomic intervals specified by a user. It also generates the maximum value in the table as a separate file with a “.max” extension.
Syntax: 
```python FRAGMAP-TABLE.py <TSR.bed file> < Mapped-fragments.bed file> <number of TSRs>```

### Parameter description:
TSR.bed file: provide genomic intervals of the same size or a genomic interval in a bed file format. Please keep the file extension as “.bed”.
Mapped-fragments.bed file: provide mapped fragments in a bed file format. Please keep the file extension as “.bed”.
number of TSRs: provide the total number of genomic intervals in the TSR.bed file.

Please use the EXAMPLE folder to run this example.
USAGE example: 
```python FRAGMAP-TABLE.py EXAMPLE/intervals.bed EXAMPLE/mapped-fragments.bed 11```

Second, the TICKMARKS-3px-GENOMICINTERVALS program adds major and minor tickmarks of user-specific length to the bottom and right axis of the data table output from the FRAGMAP-TABLE program.  The width of the tickmarks remain 3px wide in this program and the width of the tickmarks remain 5px wide in the TICKMARKS-5px-GENOMICINTERVALS program. The tickmark program duplicates the rows, and columns of the data table as specified by the user for the final image. 
Syntax: 
```python TICKMARKS-3px-GENOMICINTERVALS.py <Mapped-fragments.combined.txt> <fragMap height> < fragMap width> < fragMap tick length> <Mapped-fragments.combined.max>```

### Parameter description:
Mapped-fragments.combined.txt is the output file from FRAGMAP-TABLE.py.
fragMap height and width, and tick length are user specified parameters.
Mapped-fragments.combined.max is the output file from FRAGMAP-TABLE.py.

Please use the EXAMPLE folder to run this example.
USAGE example: 
```python TICKMARKS-3px-GENOMICINTERVALS.py EXAMPLE/intervals-mapped-fragments.combined.txt 2 2 12 EXAMPLE/intervals-mapped-fragments.combined.max```

Finally, the Rscript FMAP.R makes the fragMap image from the output of the tickmark program.
Syntax: 
```Rscript FMAP.R <Mapped-fragments.combined.csv> <Mapped-fragments.combined.max>```

### Parameter description:
Mapped-fragments.combined.csv is the output file from TICKMARKS-3px-GENOMICINTERVALS.py.
Mapped-fragments.combined.max is the output file from FRAGMAP-TABLE.py.
Please use the EXAMPLE folder to run this example.
USAGE example: Rscript FMAP.R EXAMPLE/intervals-mapped-fragments.combined.csv EXAMPLE/intervals-mapped-fragments.combined.max

### Output:
A fragMap tiff image file is the output of this program.
