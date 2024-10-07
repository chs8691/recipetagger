# Long running tests on image files
import pytest
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


@pytest.mark.parametrize("cam", cameras)
def test_images_iso(cam):

    attribute = 'ISO'
    r = R.ISO

    for (n,v) in [
        ('3200-Auto', 3200),
        ('6400', 6400),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_clarity(cam):

    attribute = 'Clarity'
    r = R.CLARITY

    for (n,v) in [
        ('-5', -5),
        ('+5', 5),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_noise_reduction(cam):

    attribute = 'NoiseReduction'
    r = R.HIGH_ISONR

    for (n,v) in [
        ('-4', -4),
        ('+4', 4),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_wb_color_temperature(cam):
 
    attribute = 'WB'
    n = 'ColorTemperature'

            
    for (nk, vk, nf, vr, vb) in [
        ('4350K', 4350, '', 0, 0),
        ('5500K', 5500, '-R-1-B+2', -1, 2),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}-{n}-{nk}{nf}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[R.KELVIN] == vk, name   
        assert act[R.WHITE_BALANCE_R] == vr , name   
        assert act[R.WHITE_BALANCE_B] == vb , name   


@pytest.mark.parametrize("cam", cameras)
def test_images_wb_fine_tune(cam):
 
    attribute = 'WB'

    for (n, v, nr, vr, nb, vb) in [
        ('Auto', WB.AUTO, '+9', 9, '-9', -9),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}-{n}-R{nr}-B{nb}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[R.WHITE_BALANCE_R] == vr , name   
        assert act[R.WHITE_BALANCE_B] == vb , name   


@pytest.mark.parametrize("cam", cameras)
def test_images_wb_simple(cam):
 
    attribute = 'WB'
    r = R.WHITE_BALANCE
            
    for (n, v) in [
        ('Auto', WB.AUTO),
        ('AutoAmbiencePriority', WB.AMBIENCE_PRIORITY),
        ('AutoWhitePriority', WB.WHITE_PRIORITY),
        ('Daylight', WB.DAYLIGHT),
        ('Shade', WB.SHADE),
        ('Fluorescent1', WB.FLUORESCENT1),
        ('Fluorescent2', WB.FLUORESCENT2),
        ('Fluorescent3', WB.FLUORESCENT3),
        ('Incandescent', WB.INCANDESENT),
        ('Underwater', WB.UNDERWATER),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}-{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name  


@pytest.mark.parametrize("cam", cameras)
def test_images_color_chrome_effects(cam):
 
    attribute = 'CC'
    r = R.CCR_EFFECT
    r2 = R.CCRFX_BLUE

    for (n,v, v2) in [
        ('off-weak', CC.OFF, CC.WEAK),
        ('strong-off', CC.STRONG, CC.OFF),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}-{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name   
        assert act[r2] == v2 , name   


@pytest.mark.parametrize("cam", cameras)
def test_images_grain(cam):

    attribute = 'Grain'
    r = R.GRAIN_EFFECT

    for (n,v) in [
        ('off', G.OFF),
        ('strong-small', G.STRONG_SMALL),
        ('weak-large', G.WEAK_LARGE),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}-{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_sharpness(cam):

    attribute = 'Sharpness'
    r = R.SHARPNESS

    for (n,v) in [
        ('-4', -4),
        ('+4', 4),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_saturation(cam):

    attribute = 'Saturation'
    r = R.COLOR

    for (n,v) in [
        ('-4', -4),
        ('+4', 4),
    ]:

        name = f'testdata/{cam}/{cam}-{attribute}{n}.JPG'

        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)

        assert act[r] == v , name


@pytest.mark.parametrize("cam", cameras)
def test_images_drp_strong(cam):

    name = f'testdata/{cam}/{cam}-DRP-Strong.JPG'

    if not path.exists(name):
        LOGGER.warning(f'Missing test image: {name}')
        return
    
    act = reciper.read_file(name)

    assert act[R.DRANGE_PRIORITY] == DP.STRONG , name


@pytest.mark.parametrize("cam", cameras)
def test_images_drp_auto(cam):

    name = f'testdata/{cam}/{cam}-DRP-Strong.JPG'

    if not path.exists(name):
        LOGGER.warning(f'Missing test image: {name}')
        return
    
    act = reciper.read_file(name)

    assert act[R.DRANGE_PRIORITY] == DP.STRONG , name


@pytest.mark.parametrize("cam", cameras)
def test_images_dr_400(cam):

    name = f'testdata/{cam}/{cam}-DR-400.JPG'

    if not path.exists(name):
        LOGGER.warning(f'Missing test image: {name}')
        return
    
    act = reciper.read_file(name)

    assert R.DRANGE_PRIORITY not in act , name
    assert act[R.DYNAMIC_RANGE] == DR.DR400 , name
    assert act[R.HIGHLIGHTS] == 0 , name
    assert act[R.SHADOWS] == 0  , name


@pytest.mark.parametrize("cam", cameras)
def test_images_dr_auto(cam):
        
    name = f'testdata/{cam}/{cam}-DR-Auto.JPG'
    if not path.exists(name):
        LOGGER.warning(f'Missing test image: {name}')
        return
    
    act = reciper.read_file(name)

    assert R.DRANGE_PRIORITY not in act , name
    assert act[R.DYNAMIC_RANGE] == DR.DR100 , name
    assert act[R.HIGHLIGHTS] == 0 , name
    assert act[R.SHADOWS] == 0  , name


@pytest.mark.parametrize("cam", cameras)
def test_images_fs_bw(cam):
   
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
    
        name = f'testdata/{cam}/{cam}-FS-{name}.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue
    
        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == fs

        if ft is None:
            assert R.BW_FILTER not in act , name
        else:
            assert act[R.BW_FILTER] == ft , name


@pytest.mark.parametrize("cam", cameras)
def test_images_fs_color(cam):

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
        match cam:
            case X_S10:
                if f in [FS.REALA_ACE,
                            FS.NOSTALGIC_NEG]:
                    continue                

        name = f'testdata/{cam}/{cam}-FS-{f}.JPG'
        if not path.exists(name):
            LOGGER.warning(f'Missing test image: {name}')
            continue

        act = reciper.read_file(name)
        assert act[R.FILMSIMULATION] == f , name

        
