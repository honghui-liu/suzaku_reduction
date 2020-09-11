import subprocess as sp
import os
import handle_files as hf

def runcom(string):
    sp.check_call(string, shell=True)

def select_lc(data_dir, evt_list, region, outname="test.lc", binsize=10.0):
    
    os.chdir(data_dir)

    if os.path.isfile(outname):
        print(f"{outname} already exits, going to hide it!")
        cmd = f"mv {outname} .{outname}"
        runcom(cmd)

    mkf = "SAA_HXD==0 && T_SAA_HXD>436 && ELV> 5 && DYE_ELV>20 && COR>6"
    work_dir = data_dir
    events = ""
    for element in evt_list:
        events = events + element + " "
    events = events.strip()
    comm = f"""xselect <<EOF
xsel
no
read events "{events}"
{work_dir}
select mkf "{mkf}"
{work_dir}
set binsize {binsize}
filter region {region}
extract curve
save curve {outname}
exit
no
"""
    
    runcom(comm)

    cmd = "rm -f xselect.log"
    runcom(cmd)
    return outname

def select_spec(data_dir, evt_list, region, outname="test.pha"):

    os.chdir(data_dir)

    if os.path.isfile(outname):
        print(f"{outname} already exits, going to hide it!")
        cmd = f"mv {outname} .{outname}"
        runcom(cmd)

    mkf = "SAA_HXD==0 && T_SAA_HXD>436 && ELV> 5 && DYE_ELV>20 && COR>6"
    work_dir = data_dir
    events = ""
    for element in evt_list:
        events = events + element + " "
    events = events.strip()
    comm = f"""xselect <<EOF
xsel
no
read events "{events}"
{work_dir}
select mkf "{mkf}"
{work_dir}
filter region {region}
extract spec
save spec {outname}
no
exit
no
"""
    
    runcom(comm)

    cmd = "rm -f xselect.log"
    runcom(cmd)
    return outname


def select_all(data_dir, all_list, region_list):
    """
    Extract lightcurve and spectra with 'Xselect'

    Parameter
    ------
    all_list: list
        XIS cleaned event files
    """

    xi0_list, xi1_list, xi3_list = hf.arrange_list(evt_list=all_list)
    xi0_reg = region_list[0]
    xi1_reg = region_list[1]
    xi3_reg = region_list[2]

    xi0_spec = []
    xi1_spec = []
    xi3_spec = []
    
    if len(xi0_list)>0.1:
        select_lc(data_dir=data_dir, evt_list=xi0_list, region=xi0_reg[0], outname="xi0.lc")
        select_spec(data_dir=data_dir, evt_list=xi0_list, region=xi0_reg[0], outname="xi0_src.pha")
        select_spec(data_dir=data_dir, evt_list=xi0_list, region=xi0_reg[1], outname="xi0_bkg.pha")
        xi0_spec.append("xi0_src.pha")
        xi0_spec.append("xi0_bkg.pha")

    if len(xi1_list)>0.1:
        select_lc(data_dir=data_dir, evt_list=xi1_list, region=xi1_reg[0], outname="xi1.lc")
        select_spec(data_dir=data_dir, evt_list=xi1_list, region=xi1_reg[0], outname="xi1_src.pha")
        select_spec(data_dir=data_dir, evt_list=xi1_list, region=xi1_reg[1], outname="xi1_bkg.pha")
        xi1_spec.append("xi1_src.pha")
        xi1_spec.append("xi1_bkg.pha")

    if len(xi3_list)>0.1:
        select_lc(data_dir=data_dir, evt_list=xi3_list, region=xi3_reg[0], outname="xi3.lc")
        select_spec(data_dir=data_dir, evt_list=xi3_list, region=xi3_reg[0], outname="xi3_src.pha")
        select_spec(data_dir=data_dir, evt_list=xi3_list, region=xi3_reg[1], outname="xi3_bkg.pha")
        xi3_spec.append("xi3_src.pha")
        xi3_spec.append("xi3_bkg.pha")

    return xi0_spec, xi1_spec, xi3_spec


if __name__=="__main__":
    data_dir = "/home/honghui/project/XRBs/cygx1/su_pipe"
    #region = "xi1_src_pilecorr.reg"
    region = "xi1_bkg.reg"
    evt_list = ['xi1_0_3x3b_attcorr_cl.evt', 'xi1_0_5x5b_attcorr_cl.evt', 'xi1_0_5x5n_attcorr_cl.evt']
    select_spec(data_dir, evt_list, region, outname="test_bkg.pha")
