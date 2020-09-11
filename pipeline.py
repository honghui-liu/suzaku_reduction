import os
import subprocess as sp

def runcom(string):
    sp.check_call(string, shell=True)

def pipeline(indir, outdir, stem):
    logfile = outdir + '/pipeline.log'

    if os.path.isdir(outdir):
        runcom("rm " + outdir + "/*")
    else:
        runcom("mkdir " + outdir)

    comm = 'aepipeline indir={0} outdir={1} steminputs=ae{2} entry_stage=1 exit_stage=2 clobber=yes instrument=ALL > {3} 2>&1'.format(indir, outdir, stem, logfile)
    runcom(comm)

if (__name__=='__main__'):
    indir = '/home/honghui/mrk1239/702031010'
    outdir = '/home/honghui/mrk1239/test2'
    stem = '702031010'

    pipeline(indir, outdir, stem)
