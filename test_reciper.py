import pytest
from reciper import map_filmsimulation
from reciper import read_file
from reciper import map_exif_filmsimulation
import constants.recipefields as R
import constants.filmsimulations as FS


# def test_read_file_nostalgic_neg():
#     act = read_file('testdata/x-t50-nostalgic_neg.JPG')
    
#     assert act[R.FILMSIMULATION] == FS.NOSTALGIC_NEG

def test_map_exif_filmsimulation():
    
    assert map_exif_filmsimulation(0) == FS.PROVIA
    assert map_exif_filmsimulation(288) == FS.ASTIA
    assert map_exif_filmsimulation(1024) == FS.VELVIA
    assert map_exif_filmsimulation(1280) == FS.PRO_NEG_STD
    assert map_exif_filmsimulation(1281) == FS.PRO_NEG_HI
    assert map_exif_filmsimulation(1536) == FS.CLASSIC_CHROME
    assert map_exif_filmsimulation(1792) == FS.ETERNA
    assert map_exif_filmsimulation(2048) == FS.CLASSIC_NEG
    assert map_exif_filmsimulation(2304) == FS.ETERNA_BLEACH_BYPASS
    assert map_exif_filmsimulation(2560) == FS.NOSTALGIC_NEG
    assert map_exif_filmsimulation(2816) == FS.REALA_ACE
    assert map_exif_filmsimulation(9999) == None


def test_map_filmsimulation_classic_chrome():

    exp=FS.CLASSIC_CHROME

    assert map_filmsimulation('classic  chrome') == exp
    assert map_filmsimulation('CLASSiC  CHROMe') == exp

    exp=None

    assert map_filmsimulation('classic  chrom') == exp
    assert map_filmsimulation('CLASSIC_CHROME') == exp

def test_map_filmsimulation_pro_neg_std():

    exp=FS.PRO_NEG_STD

    assert map_filmsimulation('pro neg std') == exp
    assert map_filmsimulation('pro neg std.') == exp
    assert map_filmsimulation('PRO NEG STD.') == exp
    assert map_filmsimulation('PRO NEG. STD.') == exp