import pytest
from reciper import map_filmsimulation
from reciper import extract_recipe_data
from reciper import map_exif_filmsimulation
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.colorchrome as CC
import constants.dynamicrangepriority as DP
import constants.dynamicrange as DR
import constants.whitebalance as WB
import constants.sensor as SR

def test_extract_recipe_data():
    
    row = {"Name"                   :"Recipe Nr. 1",
           "Publisher"              :"Max Morytz",
           "X-Trans"                :"V",
           "Film Simulation"        :"Astia",
           "BW Color WC"            :"",
           "BW Color MC"            :"",
           "Grain Effect"           :"weak/small",
           "CCR Effect"             :"strong",
           "CCR FX Blue"            :"off",
           "White Balance"          :"Auto",
           "Kelvin"                 :"",
           "White Balance R"        :"-1",
           "White Balance B"        :"+1",
           "Dynamic Range"          :"Auto",
           "Dynamic Range Priority" :"",
           "Highlights"             :"-1",
           "Shadows"                :"+1",
           "Color"                  :"0",
           "Sharpness"              :"-2",
           "High ISO NR"            :"+2",
           "Clarity"                :"-3",
           "ISO min"                :"",
           "ISO max"                :"3200"
           }
    
    r = extract_recipe_data(row)

    assert r[R.NAME] == 'Recipe Nr. 1'
    assert r[R.PUBLISHER] == 'Max Morytz'
    assert r[R.XTRANS_VERSION] == 'V'
    assert r[R.FILMSIMULATION] == FS.ASTIA
    assert r[R.GRAIN_EFFECT] == G.WEAK_SMALL
    assert r[R.WHITE_BALANCE] == WB.AUTO
    assert r[R.WHITE_BALANCE_R] == -1
    assert r[R.WHITE_BALANCE_B] == 1
    assert r[R.DYNAMIC_RANGE] == DR.AUTO
    assert r[R.HIGHLIGHTS] == -1
    assert r[R.SHADOWS] == 1
    assert r[R.COLOR] == 0 
    assert r[R.SHARPNESS] == -2
    assert r[R.HIGH_ISONR] == 2
    assert r[R.CLARITY] == -3
    assert r[R.ISO_MIN] == 0
    assert r[R.ISO_MAX] == 3200



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


def test_map_filmsimulation():

    exp=FS.CLASSIC_CHROME

    assert map_filmsimulation('classic  chrome') == exp
    assert map_filmsimulation('CLASSiC  CHROMe') == exp

    exp=None

    assert map_filmsimulation('classic  chrom') == exp
    assert map_filmsimulation('CLASSIC_CHROME') == exp

    exp=FS.PRO_NEG_STD

    assert map_filmsimulation('pro neg std') == exp
    assert map_filmsimulation('pro neg std.') == exp
    assert map_filmsimulation('PRO NEG STD.') == exp
    assert map_filmsimulation('PRO NEG. STD.') == exp

    exp=FS.ASTIA

    assert map_filmsimulation('astia') == exp