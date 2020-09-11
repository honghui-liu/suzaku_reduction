import subprocess as sp
import os
import handle_files as hf
from astropy.io import fits
 

def runcom(string):
    sp.check_call(string, shell=True)

def get_position(evt_file):
    ra = ""
    dec = ""

    with fits.open(evt_file) as hdul:
        ra = hdul[0].header["RA_OBJ"]
        dec = hdul[0].header["DEC_OBJ"]

    return ra, dec

def xisrmfgen(phafile, outfile):
    print(f"Calculating RMF for {phafile}")
    cmd = (f"xisrmfgen phafile={phafile} outfile={outfile} >> rmf.log 2>&1")
    print(cmd)
    runcom(cmd)

    return outfile

def xissimarfgen(instrument, ra, dec, region, arf, phafile, gtifile, att, rmf):
    """
    Generate arf file for point source

    Parameter
    ------
    instrument: str
        XIS0, XIS1, XIS3

    reg: str
        source region file name


    Reference 
    """
    print(f"Calculating ARF for {phafile}")
    cmd = (f"xissimarfgen clobber=yes instrume={instrument} source_mode=J2000 "
           f"source_ra={ra} source_dec={dec} num_region=1 "
           f"region_mode=SKYREG regfile1={region} arffile1={arf} "
           f"limit_mode=NUM_PHOTON num_photon=400000 phafile={phafile} "
           f"detmask=none gtifile={gtifile} attitude={att} "
           f"rmffile={rmf} estepfile=default >> arf.log 2>&1")
    print(cmd)
    runcom(cmd)

def all_response(region_list, pha_list, evt_list, att):

    xi0_list, xi1_list, xi3_list = hf.arrange_list(evt_list)

    instruments = ["XIS0", "XIS1", "XIS3"]
    #ra, dec = get_position(evtfile)
    regions = hf.source(region_list) 
    arfs = ["xi0.arf", "xi1.arf", "xi3.arf"]
    phafiles = hf.source(pha_list)
    gtifiles = hf.source([xi0_list, xi1_list, xi3_list])
    att = att
    rmfs = ["xi0.rmf", "xi1.rmf", "xi3.rmf"]

    for i in range(3):
        if phafiles[i] != "":
            xisrmfgen(phafiles[i], rmfs[i])
            ra, dec = get_position(gtifiles[i])
            xissimarfgen(instrument=instruments[i], ra=ra, dec=dec, region=regions[i], 
                         arf=arfs[i], phafile=phafiles[i], gtifile=gtifiles[i], 
                         att=att, rmf=rmfs[i])

if __name__=="__main__":
    print("Creating response")
