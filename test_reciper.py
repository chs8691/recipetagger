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
import constants.bwfilter as BWF
from os import path

import logging

LOGGER = logging.getLogger(__name__)


# Names for building the path the test images. 
# See README file in testdata for more information.
X_T50 = 'X-T50'
X_S10 = 'X-S10'
cameras = [X_T50, X_S10]

def test_images_color_chrome_effects():
    assert 'TBC' == 'TODO'

def test_images_grain():

    attribute = 'Grain'
    r = R.GRAIN_EFFECT

    for c in cameras:

        for (n,v) in [
            ('off', G.OFF),
            ('strong-small', G.STRONG_SMALL),
            ('weak-large', G.WEAK_LARGE),
        ]:

            name = f'testdata/{c}/{c}-{attribute}-{n}.JPG'

            if not path.exists(name):
                LOGGER.warning(f'Missing test image: {name}')
                continue
        
            act = reciper.read_file(name)

            assert act[r] == v , name


def test_images_sharpness():

    attribute = 'Sharpness'
    r = R.SHARPNESS

    for c in cameras:

        for (n,v) in [
            ('-4', -4),
            ('+4', 4),
        ]:

            name = f'testdata/{c}/{c}-{attribute}{n}.JPG'

            if not path.exists(name):
                LOGGER.warning(f'Missing test image: {name}')
                continue
        
            act = reciper.read_file(name)

            assert act[r] == v , name


def test_images_saturation():

    attribute = 'Saturation'
    r = R.COLOR

    for c in cameras:

        for (n,v) in [
            ('-4', -4),
            ('+4', 4),
        ]:

            name = f'testdata/{c}/{c}-{attribute}{n}.JPG'

            if not path.exists(name):
                LOGGER.warning(f'Missing test image: {name}')
                continue
        
            act = reciper.read_file(name)

            assert act[r] == v , name


def test_images_drp_strong():

    for c in cameras:
        name = f'testdata/{c}/{c}-DRP-Strong.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert act[R.DRANGE_PRIORITY] == DP.STRONG , name


def test_images_drp_auto():

    for c in cameras:
        name = f'testdata/{c}/{c}-DRP-Strong.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert act[R.DRANGE_PRIORITY] == DP.STRONG , name


def test_images_dr_400():

    for c in cameras:
        name = f'testdata/{c}/{c}-DR-400.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert R.DRANGE_PRIORITY not in act , name
        assert act[R.DYNAMIC_RANGE] == DR.DR400 , name
        assert act[R.HIGHLIGHTS] == 0 , name
        assert act[R.SHADOWS] == 0  , name


def test_images_dr_auto():
   for c in cameras:
        
        name = f'testdata/{c}/{c}-DR-Auto.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
      
        act = reciper.read_file(name)

        assert R.DRANGE_PRIORITY not in act , name
        assert act[R.DYNAMIC_RANGE] == DR.DR100 , name
        assert act[R.HIGHLIGHTS] == 0 , name
        assert act[R.SHADOWS] == 0  , name


def test_images_fs_bw():
   
   for c in cameras:
        
        for (fs, ft) in[
            (FS.ACROS, None),
            (FS.ACROS, BWF.RED),
            (FS.MONOCHROME, None),
            (FS.MONOCHROME, BWF.YELLOW),
        ]:
            if ft is None:
                name =  fs
            else:
                name = fs + '+' + ft
        
            name = f'testdata/{c}/{c}-FS-{name}.JPG'
            if not path.exists(name):
                LOGGER.warning(f'Missing test image: {name}')
                continue
        
            act = reciper.read_file(name)
            assert act[R.FILMSIMULATION] == fs

            if ft is None:
                assert R.BW_FILTER not in act , name
            else:
                assert act[R.BW_FILTER] == ft , name


def test_images_fs_color():

   for c in cameras:
        
        for f in [
            FS.ASTIA,
            FS.PROVIA ,
            FS.CLASSIC_CHROME ,
            FS.CLASSIC_NEG ,
            FS.ETERNA ,
            FS.ETERNA_BLEACH_BYPASS ,
            FS.NOSTALGIC_NEG ,
            FS.PROVIA ,
            FS.PRO_NEG_HI ,
            FS.PRO_NEG_STD ,
            FS.REALA_ACE ,
            FS.VELVIA,
            ]:

            # Skip non existing filmsimulations
            match c:
                case X_S10:
                    if f in [FS.REALA_ACE,
                             FS.NOSTALGIC_NEG]:
                        continue                

            name = f'testdata/{c}/{c}-FS-{f}.JPG'
            if not path.exists(name):
                LOGGER.warning(f'Missing test image: {name}')
                continue

            act = reciper.read_file(name)
            assert act[R.FILMSIMULATION] == f , name

        
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

def test_exif_sharpness():
    assert ex.map_sharpness(0) == -4
    assert ex.map_sharpness(1) == -3
    assert ex.map_sharpness(2) == -2
    assert ex.map_sharpness(3) == 0
    assert ex.map_sharpness(4) == 2
    assert ex.map_sharpness(5) == 3
    assert ex.map_sharpness(6) == 4
    assert ex.map_sharpness(130) == -1 
    assert ex.map_sharpness(132) == 1

def test_exif_map_clarity():
    assert ex.map_clarity(0) == 0
    assert ex.map_clarity(-1000) == -1
    assert ex.map_clarity(-5000) == -5
    assert ex.map_clarity(1000) == 1
    assert ex.map_clarity(5000) == 5

def test_exif_map_noisereduction():
    assert ex.map_noisereduction(0) == 0
    assert ex.map_noisereduction(256) == 2
    assert ex.map_noisereduction(384) == 1
    assert ex.map_noisereduction(448) == 3
    assert ex.map_noisereduction(480) == 4
    assert ex.map_noisereduction(512) == -2
    assert ex.map_noisereduction(640) == -1
    assert ex.map_noisereduction(704) == -3
    assert ex.map_noisereduction(736) == -4


def test_exif_map_saturation():
    assert ex.map_saturation(0) == 0
    assert ex.map_saturation(128) == 1
    assert ex.map_saturation(256) == 2
    assert ex.map_saturation(192) == 3
    assert ex.map_saturation(224) == 4
    assert ex.map_saturation(384) == -1
    assert ex.map_saturation(1024) == -2
    assert ex.map_saturation(1216) == -3
    assert ex.map_saturation(1248) == -4
    assert ex.map_saturation(768) == (FS.MONOCHROME, None)
    assert ex.map_saturation(769) == (FS.MONOCHROME, BWF.RED)
    assert ex.map_saturation(770) == (FS.MONOCHROME, BWF.YELLOW)
    assert ex.map_saturation(771) == (FS.MONOCHROME, BWF.GREEN)
    assert ex.map_saturation(784) == (FS.SEPIA, None)
    assert ex.map_saturation(1280) == (FS.ACROS, None)
    assert ex.map_saturation(1281) == (FS.ACROS, BWF.RED)
    assert ex.map_saturation(1282) == (FS.ACROS, BWF.YELLOW)
    assert ex.map_saturation(1283) == (FS.ACROS, BWF.GREEN)


def test_exif_map_color_chrome():
    assert ex.map_color_chrome(0) == CC.OFF
    assert ex.map_color_chrome(1) == None
    assert ex.map_color_chrome(16) == CC.WEAK
    assert ex.map_color_chrome(32) == CC.STRONG


def test_exif_map_grain():
    assert ex.map_grain(0, 0) == G.OFF
    assert ex.map_grain(1, 1) == None
    assert ex.map_grain(32, 16) == G.WEAK_SMALL
    assert ex.map_grain(32, 32) == G.WEAK_LARGE
    assert ex.map_grain(64, 16) == G.STRONG_SMALL
    assert ex.map_grain(64, 32) == G.STRONG_LARGE


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
    assert ex.map_filmsimulation(512) == FS.VELVIA
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