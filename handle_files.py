"""
To get some necessay information (obs mode, source position)
from pipeline product
"""

import os
import glob


def clean_list(outdir):
    """
    Get the list of cleaned event list

    Parameter
    ------
    outdir: str 
        The directory where pipeline outputs are stored

    Return
    ------
    evt_list: list
        A list of cleaned event files
    """
    
    os.chdir(outdir)

    xis_cam_list = ['xi0', 'xi1', 'xi3']
    hxd_cam_list = ['pinno', 'gsono']

    xis_list = []
    hxd_list = []

    all_evtfile = glob.glob("*cl.evt")
    
    for evt in all_evtfile:
        if evt.split('_')[0][-3:] in xis_cam_list:
            xis_list.append(evt)
        elif evt.split('_')[2] in hxd_cam_list:
            hxd_list.append(evt)
    
    return xis_list, hxd_list

def arrange_list(evt_list):
    """
    Rearrange the cleaned event list according to XIS cameras

    Parameters:
    ------
    evt_list: list
        input files
    
    Return:
    ------
    xis0, xis1, xis3
    """
    
    xis0_list = []
    xis1_list = []
    xis3_list = []

    for element in evt_list:
        if 'xi0' in element:
            xis0_list.append(element)
        elif 'xi1' in element:
            xis1_list.append(element)
        elif 'xi3' in element:
            xis3_list.append(element)

    return xis0_list, xis1_list, xis3_list

def arrange_hxd(evt_list):
    pin = []
    gso = []
    for element in evt_list:
        if 'pinno' in element:
            pin.append(element)
        elif 'gsono' in element:
            gso.append(element)

    return pin, gso

def find_3x3(evt_list):

    xi_3x3_list = []

    for element in evt_list:
        if '3x3' in element:
            xi_3x3_list.append(element)

    return xi_3x3_list

def source(all_region):
    """
    Get source region file, store in a list
    """
    source_region = []
    for i in range(len(all_region)):
        if len(all_region[i])>0.1:
            source_region.append(all_region[i][0])
        else:
            source_region.append("")

    return source_region

def get_att(outdir):
    os.chdir(outdir)
    att = glob.glob("*.att")[0]

    return att

if __name__=='__main__':
    outdir = '/home/honghui/mrk1239/test'
    #print(clean_list(outdir)[0])
#    evt_list = ["xi1_0_3x3b_attcorr_cl.evt", "xi1_0_5x5b_attcorr_cl.evt", "xi1_0_5x5n_attcorr_cl.evt"]
#    xi0, xi1, xi3 = arrange_list(evt_list)
#    print(xi0)
#    print(xi1)
#    print(xi3)
    xi0_reg = ["0.reg", "1.reg"]
    xi1_reg = []
    xi3_reg = ["3.reg", "4.reg"]
    all_reg = [xi0_reg, xi1_reg, xi3_reg]
    print(source_reg(all_reg))

