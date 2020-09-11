import subprocess as sp
import os
import correction
import handle_files as hf

def runcom(string):
    sp.check_call(string, shell=True)

def viewregion(fits, src_reg, bkg_reg, cmap='heat'):
    """
    Check the region visually
    """
    
    string = (f"ds9 {fits} -regions load {src_reg} "
              f"-regions load {bkg_reg} -cmap {cmap} -log")
    runcom(string)

    return True

def pileup_region_exclude(src_reg, pile_reg):
    
    region  = src_reg.split(".")[0] + "_pilecorr.reg"

    copy = f"cat {src_reg} > {region}"
    combine = f"cat {pile_reg} >> {region}"

    runcom(copy)
    runcom(combine)
    
    return region

def get_region(all_list):
    """
    Get source and background region of XIS

    Return
    ------

    """

    xi0_list, xi1_list, xi3_list = hf.arrange_list(evt_list=all_list)


    xi0_reg = []
    xi1_reg = []
    xi3_reg = []

    if len(xi0_list)>0.1:
        event = hf.find_3x3(xi0_list)

        hint = ("Choose the source region and save it with name 'xi0_src.reg' \n"
                "Choose the background region and save as 'xi0_bkg.reg' \n"
                "Use ds9 format and 'physical' coordinate! \n")
        print(hint)
        correction.viewimage(event[0])
        xi0_reg.append('xi0_src.reg')
        xi0_reg.append('xi0_bkg.reg')

        if os.path.isfile('xi0_pileup.reg'):
            src_reg = pileup_region_exclude('xi0_src.reg', 'xi0_pileup.reg')
            xi0_reg[0] = src_reg

        print("Check regions \n")
        viewregion(fits=event[0], src_reg=xi0_reg[0], bkg_reg=xi0_reg[1])

    if len(xi1_list)>0.1:
        event = hf.find_3x3(xi1_list)

        hint = ("Choose the source region and save it with name 'xi1_src.reg' \n"
                "Choose the background region and save as 'xi1_bkg.reg' \n"
                "Use ds9 format and 'physical' coordinate! \n")
        print(hint)
        correction.viewimage(event[0])
        xi1_reg.append('xi1_src.reg')
        xi1_reg.append('xi1_bkg.reg')

        if os.path.isfile('xi1_pileup.reg'):
            src_reg = pileup_region_exclude('xi1_src.reg', 'xi1_pileup.reg')
            xi1_reg[0] = src_reg

        print("Check regions \n")
        viewregion(fits=event[0], src_reg=xi1_reg[0], bkg_reg=xi1_reg[1])

    if len(xi3_list)>0.1:
        event = hf.find_3x3(xi3_list)

        hint = ("Choose the source region and save it with name 'xi3_src.reg' \n"
                "Choose the background region and save as 'xi3_bkg.reg' \n"
                "Use ds9 format and 'physical' coordinate! \n")
        print(hint)
        correction.viewimage(event[0])
        xi3_reg.append('xi3_src.reg')
        xi3_reg.append('xi3_bkg.reg')

        if os.path.isfile('xi3_pileup.reg'):
            src_reg = pileup_region_exclude('xi3_src.reg', 'xi3_pileup.reg')
            xi3_reg[0] = src_reg

        print("Check regions \n")
        viewregion(fits=event[0], src_reg=xi3_reg[0], bkg_reg=xi3_reg[1])

    return xi0_reg, xi1_reg, xi3_reg
