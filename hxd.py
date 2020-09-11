import glob
import subprocess as sp
import os
import handle_files as hf

def runcom(string):
    sp.check_call(string, shell=True)

def hxdpinxbpi(clean_evt, pse_evt, bkg):
    """
    hxdpinxbpi input_fname=ae409049010hxd_0_pinno_cl.evt 
    pse_event_fname=ae409049010hxd_0_pse_cl.evt 
    bkg_event_fname=ae409049010_hxd_pinbgd.evt.gz 
    groupspec=no clobber=yes outstem=hxdpin
    """
    cmd = (f"hxdpinxbpi input_fname={clean_evt} pse_event_fname={pse_evt} bkg_event_fname={bkg} "
           f"groupspec=no clobber=yes outstem=hxdpin > pin.log 2>&1")

    runcom(cmd)

def hxdgsoxbpi(clean_evt, pse_evt, bkg):
    cmd = (f"hxdgsoxbpi input_fname={clean_evt} pse_event_fname={pse_evt} bkg_event_fname={bkg} "
           f"groupspec=no clobber=yes outstem=hxdgso > gso.log 2>&1")

    runcom(cmd)

def hxdpin(hxd_list):
    pin, gso = hf.arrange_hxd(hxd_list)
    link = "https://heasarc.gsfc.nasa.gov/FTP/suzaku/data/background/"
    print(f"Download NXB from: {link}")
    input("Press Enter to continue...")
    if len(pin)>0.1:
        clean_evt = pin[0]
        pse_evt = glob.glob("*_pse_cl.evt")[0]
        bkg = glob.glob("*hxd_pinbgd.evt.gz")[0]
        hxdpinxbpi(clean_evt, pse_evt, bkg)

def hxdgso(hxd_list):
    pin, gso = hf.arrange_hxd(hxd_list)
    link = "https://heasarc.gsfc.nasa.gov/FTP/suzaku/data/background/"
    print(f"Download NXB from: {link}")
    input("Press Enter to continue...")
    if len(gso)>0.1:
        clean_evt = gso[0]
        pse_evt = glob.glob("*_pse_cl.evt")[0]
        bkg = glob.glob("*hxd_gsobgd.evt.gz")[0]
        hxdgsoxbpi(clean_evt, pse_evt, bkg)

if __name__=="__main__":
    workdir = "/home/honghui/project/XRBs/cygx1/su_pipe"
    xis_list, hxd_list = hf.clean_list(workdir)
    os.chdir(workdir)
    #ihxdpin(hxd_list)
    hxdgso(hxd_list)
