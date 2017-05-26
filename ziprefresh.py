#!/usr/bin/env python3
import click
import pathlib
import sys
import tempfile
import zipfile
from pathlib import Path
compmap = {'store': zipfile.ZIP_STORED,
           'deflate': zipfile.ZIP_DEFLATED,
           'bzip2': zipfile.ZIP_BZIP2,
           'lzma': zipfile.ZIP_LZMA
          }

def decompress(zfilename):
    """Decompresses a zipfile to a temporary directory and returns the directory path"""
    tpath = tempfile.TemporaryDirectory(prefix='ziprefresh_')
    with zipfile.ZipFile(zfilename, 'r') as zfile:
        zfile.extractall(str(tpath))

    return tpath

def recompress(fpath, zfilename, compression):
    with zipfile.ZipFile(zfilename, 'w', compression=compression) as zfile:
        for filename in Path(str(fpath)).iterdir():
            #click.echo(str(filename.relative_to(str(fpath))))
            zfile.write(str(filename) ,str(filename.relative_to(str(fpath))))

    return zfilename

@click.command()
@click.version_option()
@click.argument('filename')
@click.option('--compression', '-c', type=click.Choice(['store', 'deflate', 'bzip2', 'lzma']), default='deflate')
@click.option('--replace/--no-replace', default=True)
@click.option('--output', '-o', help='new output filename, only valid if --no-replace is provided', metavar='FILENAME', )
def refresh(filename, compression, replace, output):
    if replace and output:
        raise click.BadParameter('zipfile replacement is enabled, do not provide an output file')
    if not replace and not output:
        raise click.BadParameter('output filename required if replacement is disabled')


    tpath = decompress(filename)
    click.echo(tpath)

    if replace:
        output = filename
    
    zfile = recompress(tpath, output, compmap[compression])
    click.echo(zfile)
    tpath.cleanup()

