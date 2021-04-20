<!-- <p align="center">
  <img src="MetaBCC-LR_logo.png" width="600" title="Final Labelling" alt="Final Labelling">
</p> -->

# LRBinner: Binning Error-Prone Long Reads Using Auto Encoders

![GitHub](https://img.shields.io/github/license/anuradhawick/LRBinner)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/anuradhawick/LRBinner)

## Dependencies
LRBinner is coded purely using C++ (v9) and Python 3.7. To run LRBinner, you will need to install the following python and C++ modules.

### Python dependencies
* numpy 1.16.4 
* scipy 1.3.0 
* seaborn 0.9.0
* h5py 2.9.0
* tabulate 0.8.7
* pytorch 1.4.0

### C++ requirements
* GCC version 9.1.0
* OpenMP 4.5 for multi processing

### Third party programs
* DSK: https://github.com/GATB/dsk
    * Add DSK binaries to your PATH variable

## Downloading MetaBCC-LR
To download LRBinner, you have to clone the LRBinner repository to your machine.

```
git clone https://github.com/anuradhawick/LRBinner.git
```

## Compiling the source code
* Build the binaries
```
cd LRBinner
python setup.py build
```
OR
```
sh build.sh
```    
* To install the program 
```
pip install .
```
OR add the program path to your $PATH variable.

## Running the MetaBCC-LR
In order to run MetaBCC-LR you are required to provide the reads in FASTQ or FASTA format.

### Test run data

Extract test data from `test_data` folder;

```
LRBinner -r reads.fasta -o lrb_output/ --ae-epochs 200 --resume -mbs 1000 -bit 0
```

### Test run results

Note that the results could vary due to slight sampling differences. Evaluations can be done using the `eval.py` script.

```
_                         Bin-0_(2)  Bin-1_(3)  Bin-2_(1)  Bin-3_(0)  Bin-4_(4)
Campylobacter_jejuni      1          0          0          63         5726
Acetobacter_pasteurianus  592        6138       58         42         0
Yersinia_pestis_Angola    30946      255        25         370        181
Lactobacillus_paracasei   157        0          6962       100        0
Chlamydia_psittaci        0          0          0          5512       0

Precision            96.77
Recall               96.77
F1-Score             96.77
```

### Available LRBinner Commands 

Use the `-h` argument to list all the available commands.
```
cd LRBinner
./LRBinner -h
```
### Help

```
usage: LRBinner [-h] --reads-path READS_PATH [--threads THREADS]
                [--bin-size BIN_SIZE] [--bin-count BIN_COUNT]
                [--k-mer-vector {3,4,5}] [--max-memory MAX_MEMORY]
                [--ae-epochs AE_EPOCHS] [--ae-dims AE_DIMS]
                [--ae-hidden AE_HIDDEN] [--min-bin-size MIN_BIN_SIZE]
                [--bin-iterations BIN_ITERATIONS] [--separate-reads]
                [--resume] --output <DEST> [--version]

LRBinner Help. A tool developed for binning of metagenomics long reads
(PacBio/ONT). Tool utilizes composition and coverage profiles of reads based
on k-mer frequencies to perform dimension reduction via a deep variational
auto-encoder. Dimension reduced reads are then clustered using a novel 
distance histogram based clustering algorithm. Minimum RAM requirement is 9GB.

optional arguments:
  -h, --help            show this help message and exit
  --reads-path READS_PATH, -r READS_PATH
                        Reads path for binning
  --threads THREADS, -t THREADS
                        Thread count for computation
  --bin-size BIN_SIZE, -bs BIN_SIZE
                        Bin size for the coverage histogram.
  --bin-count BIN_COUNT, -bc BIN_COUNT
                        Number of bins for the coverage histogram.
  --k-mer-vector {3,4,5}, -k {3,4,5}
                        k value for k-mer frequency vector. Choose between 3
                        and 5.
  --max-memory MAX_MEMORY, -m MAX_MEMORY
                        Default 5000. DSK k-mer counter accepts a max memory
                        parameter. However, the complete pipeline requires
                        5GB+ RAM. This is only to make DSK step faster, should
                        you have more RAM.
  --ae-epochs AE_EPOCHS
                        Epochs for the auto_encoder.
  --ae-dims AE_DIMS     Size of the latent dimension.
  --ae-hidden AE_HIDDEN
                        Hidden layer sizes eg: 128,128
  --min-bin-size MIN_BIN_SIZE, -mbs MIN_BIN_SIZE
                        The minimum number of reads a bin should have.
  --bin-iterations BIN_ITERATIONS, -bit BIN_ITERATIONS
                        Number of iterations for cluster search. Use 0 for
                        exhaustive search.
  --separate-reads, -sep
                        Flag to separate reads into bins detected. Avaialbe in
                        folder named 'binned'.
  --resume              Continue from the last step or the binning step (which
                        ever comes first). Can save time needed to run DSK and
                        obtain k-mers.
  --output <DEST>, -o <DEST>
                        Output directory
  --version, -v         Show version.

```
* Output path is the foldername that you wish the results to be in.
* Specify the number of threads
<!-- 
## Citation

```
TBD
``` -->

## Notes

CODE IS UNDER CLEANING! CHANGES WILL FOLLOW
