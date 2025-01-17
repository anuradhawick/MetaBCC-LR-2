#!/usr/bin/env python
import argparse
import os
import sys
import time
import logging
import shutil

from mbcclr_utils import pipelines


def main():
    common_arg_parser = argparse.ArgumentParser(add_help=False)

    common_arg_parser.add_argument('--reads-path', '-r',
                        help="Reads path for binning",
                        type=str,
                        required=True)
    common_arg_parser.add_argument('--k-size', '-k',
                        help="k value for k-mer frequency vector. Choose between 3 and 5.",
                        type=int,
                        required=False,
                        choices=[3, 4, 5],
                        default=3)
    common_arg_parser.add_argument('--bin-size', '-bs',
                        help="Bin size for the coverage histogram.",
                        type=int,
                        required=False,
                        default=10)
    common_arg_parser.add_argument('--bin-count', '-bc',
                        help="Number of bins for the coverage histogram.",
                        type=int,
                        required=False,
                        default=32)
    common_arg_parser.add_argument('--ae-epochs',
                        help="Epochs for the auto_encoder.",
                        type=int,
                        required=False,
                        default=200)
    common_arg_parser.add_argument('--ae-dims',
                        help="Size of the latent dimension.",
                        type=int,
                        required=False,
                        default=8)
    common_arg_parser.add_argument('--ae-hidden',
                        help="Hidden layer sizes eg: 128,128",
                        type=str,
                        required=False,
                        default="128,128")
    common_arg_parser.add_argument('--threads', '-t',
                        help="Thread count for computations",
                        type=int,
                        default=8,
                        required=False)
    common_arg_parser.add_argument('--separate', '-sep',
                        help="Flag to separate reads/contigs into bins detected. Avaialbe in folder named 'binned'.",
                        action='store_true')
    common_arg_parser.add_argument('--cuda',
                        action='store_true',
                        help='Whether to use CUDA if available.'
                        )
    common_arg_parser.add_argument('--resume',
                        action='store_true',
                        help='Continue from the last step or the binning step (which ever comes first). Can save time needed count k-mers.'
                        )
    common_arg_parser.add_argument('--output', '-o', metavar='<DEST>',
                        help="Output directory", type=str, required=True)

    main_arg_parser = argparse.ArgumentParser(description="""LRBinner Help. A tool developed for binning of metagenomics long reads (PacBio/ONT) and long read assemblies. \
            Tool utilizes composition and coverage profiles of reads based on k-mer frequencies to perform dimension reduction via a deep variational auto-encoder. \
            Dimension reduced reads are then clustered. Minimum RAM requirement is 9GB (4GB GPU if cuda used).""", add_help=True)
    main_arg_parser.add_argument('--version', '-v',
                        action='version',
                        help="Show version.",
                        version='%(prog)s 2.1')

    mode_parsers = main_arg_parser.add_subparsers(title="LRBinner running Mode", required=True, dest="mode")
    
    # Read binner specific arguments
    parser_read_binner = mode_parsers.add_parser('reads', parents=[common_arg_parser], help="for binning reads")
    # parser_read_binner.add_argument('--must-link', '-ml',
    #                     help="Pairs of read indices to be binned together",
    #                     type=str,
    #                     default=None,
    #                     required=False)
    # parser_read_binner.add_argument('--must-not-link', '-mnl',
    #                     help="Pairs of read indices to be binned separately",
    #                     type=str,
    #                     default=None,
    #                     required=False)
    parser_read_binner.add_argument('--min-bin-size', '-mbs',
                        help="The minimum number of reads a bin should have.",
                        type=int,
                        required=False,
                        default=10000)
    parser_read_binner.add_argument('--bin-iterations', '-bit',
                        help="Number of iterations for cluster search. Use 0 for exhaustive search.",
                        type=int,
                        required=False,
                        default=1000)

    # contig binner specific arguments
    parser_contig_binner = mode_parsers.add_parser('contigs', parents=[common_arg_parser], help="for binning contigs")
    parser_contig_binner.add_argument('--contigs', '-c',
                        help="Contigs path",
                        type=str,
                        required=True)
    
    # command line args
    args = main_arg_parser.parse_args()
    
    # running mode
    mode = args.mode
    # is resuming
    resume = args.resume

    reads_path = args.reads_path
    threads = args.threads
    cuda = args.cuda
    output = args.output

    # init logger
    logger = logging.getLogger('LRBinner')
    logger.setLevel(logging.DEBUG)

    if not resume and os.path.isdir(f"{output}"):
        shutil.rmtree(output)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    consoleHeader = logging.StreamHandler()
    consoleHeader.setFormatter(formatter)
    consoleHeader.setLevel(logging.INFO)
    logger.addHandler(consoleHeader)

    # init timer
    start_time = time.time()

    # Validation of inputs
    if not reads_path.split(".")[-1].lower() in ['fq', 'fasta', 'fa', 'fastq']:
        logger.error(
            "Unable to detect file type of reads. Please use either FASTA of FASTQ. Good Bye!")
        sys.exit(1)

    if threads <= 0:
        print("Minimum number of threads is 1. Using thread count 1 and continue")
        threads = 1

    if not os.path.isfile(reads_path):
        print("Failed to open reads file")
        print("Exitting process. Good Bye!")
        sys.exit(1)

    if not os.path.exists(output):
        os.makedirs(output)
        os.makedirs(f"{output}/profiles")

    if not os.path.exists(f"{output}/marker_genes") and mode=='contigs':
        os.makedirs(f"{output}/marker_genes")
    
    if not os.path.exists(f"{output}/fragments") and mode=='contigs':
        os.makedirs(f"{output}/fragments")

    # Validation of inputs end

    # init logger file
    fileHandler = logging.FileHandler(f"{output}/LRBinner.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # running program
    start_time = time.time()
    logger.info("Command " + " ".join(sys.argv))

    if cuda:
        import torch
        if torch.cuda.is_available():
            cuda = True
            logger.info("CUDA found in system")
        else:
            cuda = False
            logger.info("CUDA not found in system")

    if mode == 'contigs':
        pipelines.run_contig_binning(args)
    
    if mode == 'reads':
        pipelines.run_reads_binning(args)

    end_time = time.time()
    time_taken = end_time - start_time
    logger.info(
        f"Program Finished!. Please find the output in bins.txt")
    logger.info(f"Total time consumed = {time_taken:.2f} seconds")
    logger.info(
        f"Thank you for using LRBinner. Feedback will be much appreciated!")

    logger.removeHandler(fileHandler)
    logger.removeHandler(consoleHeader)


if __name__ == '__main__':
    main()
