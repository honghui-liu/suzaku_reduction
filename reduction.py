"""
Author: Liu Honghui
Purpose: A scirpt to reduce Suzaku data

Update log:
2020.08.18 add pipeline and attitude correction


"""


import os
import argparse
import pipeline
import correction
import region
import xselect
import hxd
import response
import handle_files as hf

if (__name__ == '__main__'):
    readme = '''A script to reduce the Suzaku data
    Usage:
    ------
    python reduction.py --pathin /path/of/the/input --pathout /path/of/the/output --id obsid --update --pileup
    ------

    Parameters
    ------
    pathin: str
        Path in which the event files are stored
    pathout: str
        Path in which the output files will be stored
    id: str
        The observation ID
    --update: 
        Update photon position due to "thermal wobbling"
    --pileup: 
        Correct for pile-up effect
    '''

    os.environ['HEADASNOQUERY'] = ''
    os.environ['HEADASPROMPT'] = '/dev/null'

    parser = argparse.ArgumentParser(description=readme, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-i", "--pathin", help="Path in which the event files are stored", type=str)
    parser.add_argument("-o", "--pathout", help="Path in which the output files will be stored", type=str)
    parser.add_argument("--id", help="observation ID", type=str)
    parser.add_argument("--update", help="If to update photon position using 'aeattcor2'", action="store_true")
    parser.add_argument("--pileup", help="If to correct pileup", action="store_true")
    args = parser.parse_args()

    if (args.pathin is None or args.pathout is None or args.id is None):
        raise ValueError("The input path, output path and observation ID have to be specified!")


    print('#'*15 + ' Runing pipeline ' + '#'*15)
    #pipeline.pipeline(indir=args.pathin, outdir=args.pathout, stem=args.id)

    # get info: att, evt_list
    att = hf.get_att(args.pathout)
    xis_list, hxd_list = hf.clean_list(args.pathout)

    os.chdir(args.pathout)

    if args.update:
        print('#'*15 + ' Correct attitude file ' + '#'*15)
        new_att = correction.attcorr(args.pathout)
        print('#'*15 + ' Updating photon position ' + '#'*15)
        new_xis_list = correction.update_evt(args.pathout, new_att)
        att = new_att
        xis_list = new_xis_list

    if args.pileup:
        print('#'*15 + ' Pile-up correction ' + '#'*15)
        correction.pileup_excl(xis_list)


    print('#'*15 + ' Source and background region ' + '#'*15)
    xi0_reg, xi1_reg, xi3_reg = region.get_region(xis_list)
    all_region = [xi0_reg, xi1_reg, xi3_reg]

    print('#'*15 + ' Extract source and background spectra with Xselect ' + '#'*15)
    xi0_spec, xi1_spec, xi3_spec =xselect.select_all(data_dir=args.pathout, all_list=xis_list, region_list=all_region) 
    all_pha = [xi0_spec, xi1_spec, xi3_spec] 

    print('#'*15 + ' Creat response files ' + '#'*15)
    response.all_response(all_region, all_pha, xis_list, att)

    print('#'*15 + ' Work on HXD pin ' + '#'*15)
    hxd.hxdpin(hxd_list)

    print('#'*15 + ' Work on HXD gso ' + '#'*15)
    hxd.hxdgso(hxd_list)
