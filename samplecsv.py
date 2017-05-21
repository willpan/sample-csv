#! /usr/bin/env python
"""
samplecsv

A utility to randomly sample data from a csv file
"""
import argparse
import csv
import random
import sys


def sniff(buffer):
    """Determine if csv has header and its dialect"""
    sample = buffer.read(4098)
    buffer.seek(0)

    sniffer = csv.Sniffer()
    has_header = sniffer.has_header(sample)
    dialect = sniffer.sniff(sample)
    return has_header, dialect


def random_samples(n, seq, preserve_order=False):
    """Get n random samples from the sequence."""
    samples = []

    for idx, sample in enumerate(seq):
        if idx < n:
            samples.append((idx, sample))
        else:
            i = random.randint(0, idx)
            if i < n:
                samples[i] = (idx, sample)

    if preserve_order:
        samples = sorted(samples, key=lambda x: x[0])

    return [x[1] for x in samples]


def main(filename, n, preserve_order):
    header = None

    with open(filename) as f:
        has_header, dialect = sniff(f)

        reader = csv.reader(f, dialect=dialect)

        if has_header:
            header = next(reader)

        samples = random_samples(n, reader, preserve_order)

    # TODO: Optionally preserve order
    writer = csv.writer(sys.stdout, dialect=dialect)
    if header is not None:
        writer.writerow(header)

    for line in samples:
        writer.writerow(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A utility to randomly sample data from a csv file.')

    parser.add_argument('file', help='path to csv file to sample')
    parser.add_argument('-n', type=int, default=1000,
                        help='number of lines to sample, default 1000')
    parser.add_argument('--preserve-order', default=False, action='store_true',
                        help='keep samples in same order as in file')

    args = parser.parse_args()
    main(filename=args.file, n=args.n, preserve_order=args.preserve_order)
