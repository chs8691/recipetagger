import exifing as ex
import reciping as rp
import reciper
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.dynamicrange as DR
import constants.drangepriority as DP
import constants.whitebalance as WB
import constants.sensor as SR
import constants.colorchrome as CC
from os import path

import logging

LOGGER = logging.getLogger(__name__)


# Names for building the path the test images. 
# See README file in testdata for more information.
X_T50 = 'X-T50'
X_S10 = 'X-S10'
cameras = [X_T50, X_S10]

def test_images_drp_strong():

    for c in cameras:
        name = f'testdata/{c}/{c}-DRP-Strong.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert act[R.DRANGE_PRIORITY] == DP.STRONG


def test_images_drp_auto():

    for c in cameras:
        name = f'testdata/{c}/{c}-DRP-Strong.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert act[R.DRANGE_PRIORITY] == DP.STRONG


def test_images_dr_400():

    for c in cameras:
        name = f'testdata/{c}/{c}-DR-400.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert R.DRANGE_PRIORITY not in act
        assert act[R.DYNAMIC_RANGE] == DR.DR400
        assert act[R.HIGHLIGHTS] == 0
        assert act[R.SHADOWS] == 0 


def test_images_dr_auto():
   for c in cameras:
        
        name = f'testdata/{c}/{c}-DR-Auto.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert R.DRANGE_PRIORITY not in act
        assert act[R.DYNAMIC_RANGE] == DR.DR100
        assert act[R.HIGHLIGHTS] == 0
        assert act[R.SHADOWS] == 0 

def test_images_fs_astia():
   for c in cameras:
        
        name = f'testdata/{c}/{c}-FS-Astia.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == FS.ASTIA


def test_images_fs_acros():
   for c in cameras:
        
        name = f'testdata/{c}/{c}-FS-Acros.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == FS.ACROS



def test_images_fs_realaace():
   for c in cameras:
        
        # Exclude Cameras without this FS
        if c in [X_S10]:
            continue
   
        name = f'testdata/{c}/{c}-FS-RealaAce.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == FS.REALA_ACE


def test_images_fs_nostalgicneg():
   for c in cameras:
        
        # Exclude Cameras without this FS
        if c in [X_S10]:
            continue
   
        name = f'testdata/{c}/{c}-FS-NostalgicNeg.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == FS.NOSTALGIC_NEG


def test_map_drange_priority():
    assert ex.map_drange_priority(None) == None
    assert ex.map_drange_priority(1) == DP.WEAK
    assert ex.map_drange_priority(2) == DP.STRONG
    assert ex.map_drange_priority(3) == None


def test_map_dynamic_range():
    assert ex.map_dynamic_range(0) == DR.AUTO
    assert ex.map_dynamic_range(100) == DR.DR100
    assert ex.map_dynamic_range(200) == DR.DR200
    assert ex.map_dynamic_range(400) == DR.DR400
    

def test_exif_map_wb_finetune():
    assert ex.map_wb_finetune("0 0") == (0, 0)
    assert ex.map_wb_finetune("-1 2") == (-1, 2)
    assert ex.map_wb_finetune("19 -18") == (19, -18)
    assert ex.map_wb_finetune("20 -40") == (1, -2)


def test_exif_map_color_chrome():
    assert ex.map_color_chrome(0) == CC.OFF
    assert ex.map_color_chrome(1) == None
    assert ex.map_color_chrome(16) == CC.WEAK
    assert ex.map_color_chrome(32) == CC.STRONG


def test_exif_map_grain():
    assert ex.map_grain(0, 0) == G.OFF
    assert ex.map_grain(1, 1) == None
    assert ex.map_grain(16, 16) == G.WEAK_SMALL
    assert ex.map_grain(16, 32) == G.WEAK_LARGE
    assert ex.map_grain(32, 16) == G.STRONG_SMALL
    assert ex.map_grain(32, 32) == G.STRONG_LARGE


def test_exif_map_white_balance():
    
    assert ex.map_whitebalance(0) == WB.AUTO
    assert ex.map_whitebalance(1) == WB.WHITE_PRIORITY
    assert ex.map_whitebalance(2) == WB.AMBIENCE_PRIORITY
    assert ex.map_whitebalance(256) == WB.DAYLIGHT
    assert ex.map_whitebalance(512) == WB.SHADE
    assert ex.map_whitebalance(768) == WB.FLUORESCENT1
    assert ex.map_whitebalance(769) == WB.FLUORESCENT1
    assert ex.map_whitebalance(770) == WB.FLUORESCENT1
    assert ex.map_whitebalance(771) == WB.FLUORESCENT2
    assert ex.map_whitebalance(772) == WB.FLUORESCENT3
    assert ex.map_whitebalance(1024) == WB.INCANDESENT
    assert ex.map_whitebalance(1280) == WB.UNKNOWN
    assert ex.map_whitebalance(1536) == WB.UNDERWATER
    assert ex.map_whitebalance(3840) == WB.UNKNOWN
    assert ex.map_whitebalance(3841) == WB.UNKNOWN
    assert ex.map_whitebalance(3842) == WB.UNKNOWN
    assert ex.map_whitebalance(3843) == WB.UNKNOWN
    assert ex.map_whitebalance(3844) == WB.UNKNOWN
    assert ex.map_whitebalance(4080) == WB.KELVIN

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
           "Dynamic Range Priority" :"off",
           "Highlights"             :"-1",
           "Shadows"                :"+1",
           "Color"                  :"0",
           "Sharpness"              :"-2",
           "High ISO NR"            :"+2",
           "Clarity"                :"-3",
           "ISO min"                :"",
           "ISO max"                :"3200"
           }
    
    
    r = rp.extract_data(row)

    assert r[R.NAME] == 'Recipe Nr. 1'
    assert r[R.PUBLISHER] == 'Max Morytz'
    assert r[R.XTRANS_VERSION] == 'V'
    assert r[R.FILMSIMULATION] == FS.ASTIA
    assert R.BW_COLOR_WC not in r 
    assert R.BW_COLOR_MC not in r
    assert r[R.GRAIN_EFFECT] == G.WEAK_SMALL
    assert r[R.WHITE_BALANCE] == WB.AUTO
    assert R.KELVIN not in r 
    assert r[R.WHITE_BALANCE_R] == -1
    assert r[R.WHITE_BALANCE_B] == 1
    assert r[R.DYNAMIC_RANGE] == DR.AUTO
    assert R.DRANGE_PRIORITY not in r 
    assert r[R.HIGHLIGHTS] == -1
    assert r[R.SHADOWS] == 1
    assert r[R.COLOR] == 0 
    assert r[R.SHARPNESS] == -2
    assert r[R.HIGH_ISONR] == 2
    assert r[R.CLARITY] == -3
    assert r[R.ISO_MIN] == 0
    assert r[R.ISO_MAX] == 3200

def test_extract_recipe_data2():

    row = {"Name"                   :"Recipe Nr. 2",
           "Publisher"              :"Max Morytz",
           "X-Trans"                :"IV",
           "Film Simulation"        :"ACROS",
           "BW Color WC"            :"-1",
           "BW Color MC"            :"+1",
           "Grain Effect"           :"",
           "CCR Effect"             :"weak",
           "CCR FX Blue"            :"strong",
           "White Balance"          :"Kelvin",
           "Kelvin"                 :"10000",
           "White Balance R"        :"0",
           "White Balance B"        :"0",
           "Dynamic Range"          :"",
           "Dynamic Range Priority" :"Strong",
           "Highlights"             :"0",
           "Shadows"                :"0",
           "Color"                  :"",
           "Sharpness"              :"0",
           "High ISO NR"            :"-4",
           "Clarity"                :"1",
           "ISO min"                :"1200",
           "ISO max"                :"1600"
           }
    
    r = rp.extract_data(row)

    assert r[R.NAME] == 'Recipe Nr. 2'
    assert r[R.PUBLISHER] == 'Max Morytz'
    assert r[R.XTRANS_VERSION] == 'IV'
    assert r[R.FILMSIMULATION] == FS.ACROS
    assert r[R.BW_COLOR_WC] == -1
    assert r[R.BW_COLOR_MC] == 1
    assert r[R.GRAIN_EFFECT] == G.OFF
    assert r[R.WHITE_BALANCE] == WB.KELVIN
    assert r[R.KELVIN] == 10000
    assert r[R.WHITE_BALANCE_R] == 0
    assert r[R.WHITE_BALANCE_B] == 0
    assert R.DYNAMIC_RANGE not in r    
    assert r[R.DRANGE_PRIORITY] == DP.STRONG
    assert R.HIGHLIGHTS not in r
    assert R.SHADOWS not in r
    assert R.COLOR not in r
    assert r[R.SHARPNESS] == 0
    assert r[R.HIGH_ISONR] == -4
    assert r[R.CLARITY] == 1
    assert r[R.ISO_MIN] == 1200
    assert r[R.ISO_MAX] == 1600


# def test_read_file_nostalgic_neg():
#     act = read_file('testdata/x-t50-nostalgic_neg.JPG')
    
#     assert act[R.FILMSIMULATION] == FS.NOSTALGIC_NEG

def test_exif_map_filmsimulation():
    
    assert ex.map_filmsimulation(0) == FS.PROVIA
    assert ex.map_filmsimulation(288) == FS.ASTIA
    assert ex.map_filmsimulation(1024) == FS.VELVIA
    assert ex.map_filmsimulation(1280) == FS.PRO_NEG_STD
    assert ex.map_filmsimulation(1281) == FS.PRO_NEG_HI
    assert ex.map_filmsimulation(1536) == FS.CLASSIC_CHROME
    assert ex.map_filmsimulation(1792) == FS.ETERNA
    assert ex.map_filmsimulation(2048) == FS.CLASSIC_NEG
    assert ex.map_filmsimulation(2304) == FS.ETERNA_BLEACH_BYPASS
    assert ex.map_filmsimulation(2560) == FS.NOSTALGIC_NEG
    assert ex.map_filmsimulation(2816) == FS.REALA_ACE
    assert ex.map_filmsimulation(9999) == None


def test_recipe_map_filmsimulation():

    exp=FS.CLASSIC_CHROME

    assert rp.map_filmsimulation('classic  chrome') == exp
    assert rp.map_filmsimulation('CLASSiC  CHROMe') == exp

    exp=None

    assert rp.map_filmsimulation('classic  chrom') == exp
    assert rp.map_filmsimulation('CLASSIC_CHROME') == exp

    exp=FS.PRO_NEG_STD

    assert rp.map_filmsimulation('pro neg std') == exp
    assert rp.map_filmsimulation('pro neg std.') == exp
    assert rp.map_filmsimulation('PRO NEG STD.') == exp
    assert rp.map_filmsimulation('PRO NEG. STD.') == exp

    exp=FS.ASTIA

    assert rp.map_filmsimulation('astia') == exp