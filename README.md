# A python script for data reduction of Suzaku

This is a simple script to reduce Suzaku data. Follow the instruction printed on screen and your can get you data reduced. The script has been tested on Ubuntu 1404 with Python 3.7.7 and Heasoft 6.26.

## To use the script:

```
python reduction.py --pathin /path/of/the/input --pathout /path/of/the/output --id obsid --update --pileup
```

## Parameters:

--pathin: **full path** in which the raw data is stored (e.g. /home/somebody/409049010)

--pathout: **full path** for the pipeline output. The directory will be removed if already exists

--id: the observation ID (e.g. 409049010)

--update: **optional**, if to correct the attitude file with tool `aeattcor2` (to take care of the 'thermal wobbling').

--pileup: **optional**, if to exclude the pile-up region (if exists).

## Strategy:

* Run `aepipeline` to get cleaned event file.
* Update photon position with `aeattcor2` and `xiscoord` (if '--update' is specified).
* Estimate the pile-up region using `pileest` and save the region that will be excluded (if '--pileup' is specified).
* Get source and background region (manually) with `ds9`, the pileup region (if exists) will be excluded.
* Screen and filter cleaned event files of XIS and extract light curve, source spectra and background spectra using `xselect`.
* Creat RMF with `xisrmfgen`.
* Creat ARF with `xissimarfgen` with following settings (can be modified by editing 'response.py'):
  * source_mode=J2000
  * Source RA and DEC are obtained from key words "RA_OBJ" and "DEC_OBJ" from the header of event file.
  * limit_mode=NUM_PHOTON
  * num_photon=400000
* HXD PIN with `hxdpinxbpi`.
* HXD GSO with `hxdgsoxbpi`.

## Contact:

Please contact me (honghui_astro<-at->outlook.com) if there is anything wrong in the script.
