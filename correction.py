"""
Author: Liu Honghui
Purpose: Correction for the "wobbling" effect and pile up of Suzaku

Last editted: 2020.08.18
"""


import os
import subprocess as sp
import glob
import handle_files as hf

def find_largest_size(lis):
    
    file = lis[0]
    size = 0
    for i in range(len(lis)):
        if os.stat(lis[i]).st_size > size:
            file = lis[i]
            size = os.stat(lis[i]).st_size
    
    return file

def viewimage(evtfile, cmap='heat'):
    """
    View fits file with ds9
    """
    runcom("ds9 {0} -cmap {1} -log".format(evtfile, cmap))

def runcom(string):
    sp.check_call(string, shell=True)

def aeattcor2(old_att, new_att, evtfile, regfile):
    comm = (f"aeattcor2 {old_att} {new_att} {evtfile} {regfile} " 
            "> att_corr.log 2>&1")
    runcom(comm)

def xiscoord(infile, outfile, att):
    comm = (f"xiscoord infile={infile} outfile={outfile} attitude={new_att} "
            "pointing=KEY  >> xiscoord.log 2>&1")
    runcom(comm)

def pileest(evtfile, outmap, outreg, alpha=0.5, inreg='None', maxfrac=0.05, active='no'):
    """
    Use pileest in command line: pileest eventfile=xi0_0_3x3_attcorr_cl.evt outmap=xi0_pile
    alpha=0.5 inreg=None outreg=temp.reg maxpilefrac=0.05 interactive=no
    """

    comm = (f"pileest eventfile={evtfile} outmap={outmap} alpha={alpha} inreg={inreg} "
            f"outreg={outreg} maxpilefrac={maxfrac} interactive={active} >> pileup.log 2>&1")

    runcom(comm)

    return outreg

def attcorr(outdir):
    """
    Attitude correction

    Parameter
    ------
    outdir: str
        The directory in which the pipeline product is stored.

    Return:
    ------
    New attitude file will be generated
    new_att: str
        Name of the new attitude file

    Reference:
    ------
    [1] The ftool help file: https://heasarc.gsfc.nasa.gov/lheasoft/ftools/headas/aeattcor2.html
    [2] The ISIS script aeattcor.sl by John Davis: https://space.mit.edu/cxc/software/suzaku/aeatt.html 
    """

    os.chdir(outdir)
   
    # get the old attitude file
    old_att = glob.glob("*.att")[0]
    new_att = old_att.split('.')[0] + '_new.' + old_att.split('.')[1]
    

    if (len(glob.glob("*.att")) > 1.1):
        print("More than 1 attitude file is found! Current script only support one! \n" +  
              "Will use the first one: {0}".format(old_att))

    # get the cleaned event list
    evtfile = find_largest_size(glob.glob("*xi*3x3*cl.evt"))
    # evtfile = glob.glob("*xi*3x3*cl.evt")[0]
    regfile = 'source.reg'

    # select the source region for correction
    print("\nSelect the region source.reg and save as a ds9 region with 'physical coordinate'")
    print("WARNING: use the exact file name indicated above!") 
    viewimage(evtfile)

    comm = "aeattcor2 {0} {1} {2} {3} > att_corr.log 2>&1".format(old_att, new_att, evtfile, regfile)

    runcom(comm)

    return new_att


def update_evt(outdir, new_att):
    """
    Update the event list (photon position) with the new att file.
    
    Parameters
    ------
    new_att: str
        The new attitude file obtained with aeattcor2

    Return
    ------
    outlist: list
        A list of new event files of XIS instruments

    Reference
    ------
    xiscoord: https://heasarc.gsfc.nasa.gov/lheasoft/ftools/headas/xiscoord.txt
    """
    
    outlist = []

    xis_list, hxd_list = hf.clean_list(outdir)

    for infile in xis_list:
        outfile = infile[11:21] + '_attcorr_cl.evt'
        comm = (f"xiscoord infile={infile} outfile={outfile} attitude={new_att} "
                "pointing=KEY  >> xiscoord.log 2>&1")
        runcom(comm)
        outlist.append(outfile)

    return outlist

def pileup_excl(all_list):

    xi0_list, xi1_list, xi3_list = hf.arrange_list(evt_list=all_list)

    if len(xi0_list)>0.1:
        # event = hf.find_3x3(xi0_list)
        print("Estimating pile-up of xi0")
        pileest(evtfile=find_largest_size(xi0_list), outmap="xi0_pileup", outreg="xi0_pileup.reg")

    if len(xi1_list)>0.1:
        # event = hf.find_3x3(xi1_list)
        print("Estimating pile-up of xi1")
        pileest(evtfile=find_largest_size(xi0_list), outmap="xi1_pileup", outreg="xi1_pileup.reg")

    if len(xi3_list)>0.1:
        # event = hf.find_3x3(xi3_list)
        print("Estimating pile-up of xi3")
        pileest(evtfile=find_largest_size(xi0_list), outmap="xi3_pileup", outreg="xi3_pileup.reg")

    return True

if (__name__=='__main__'):
    outdir = '/home/honghui/mrk1239/test' 

    #attcorr(outdir)
    lis = update_evt(outdir, 'ae702031010_new.att') 
    print(lis)
