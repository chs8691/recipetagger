import pytest
from customs import read_template
from customs import create_custom
from customs import search_tag
from customs import search_propertyGroup
from constants import recipefields as R
from constants import dynamicrange as DR
from constants import recipefields as R
from constants import grain as GR
from constants import colorchrome as CC
from constants import whitebalance as WB
from constants import filmsimulations as FS
from constants import whitebalance as WB
from constants import drangepriority as DP
from constants import customfields as C

from os import path

import logging

LOGGER = logging.getLogger(__name__)


# TODO MISSING TESTS: label
    

# Names for building the path the test images. 
# See README file in testdata for more information.
X_T50 = 'X-T50'
X_S10 = 'X-S10'
cameras = [X_T50, X_S10]

# #############################################################################
# Compares X Raw Studio file content with script created content.
# Note: The FP1 file holds always all settings parameters, even if not relevant,
# e.g. WBColorTemp='6500K' for WhiteBalance='Auto'.
# #############################################################################

@pytest.mark.parametrize("cam", cameras)
def test_Expired_ECN_2_100T_with_mid_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-mid.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'Expired-ECN-2-100T.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'Expired ECN-2 100T',
              R.DYNAMIC_RANGE:DR.DR400,
              R.DRANGE_PRIORITY:DP.OFF,
              R.FILMSIMULATION:FS.ETERNA_BLEACH_BYPASS,
            #   R.BW_COLOR_WC:'0',
            #   R.BW_COLOR_MC:'0',
              R.GRAIN_EFFECT:GR.STRONG_LARGE,
              R.CCR_EFFECT:CC.STRONG,
              R.CCRFX_BLUE:CC.STRONG,
              R.WHITE_BALANCE:WB.KELVIN,
              R.WHITE_BALANCE_R:'9',
              R.WHITE_BALANCE_B:'-6',
              R.KELVIN:'6000',
              R.HIGHLIGHTS:'0.5',
              R.SHADOWS:'-1',
              R.COLOR:'1',
              R.SHARPNESS:'-3',
              R.HIGH_ISONR:'-4',
              R.CLARITY:'-4',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)

    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    # (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    # assert act_count == 1 and act_value == exp_value

    # (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    # assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value


@pytest.mark.parametrize("cam", cameras)
def test_Superia_Xtra_400_with_mid_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-mid.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'Superia-Xtra-400.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'Superia Xtra 400',
              R.DYNAMIC_RANGE:DR.DR400,
              R.DRANGE_PRIORITY:DP.OFF,
              R.FILMSIMULATION:FS.CLASSIC_NEG,
            #   R.BW_COLOR_WC:'18',
            #   R.BW_COLOR_MC:'18',
              R.GRAIN_EFFECT:GR.STRONG_SMALL,
              R.CCR_EFFECT:CC.OFF,
              R.CCRFX_BLUE:CC.WEAK,
              R.WHITE_BALANCE:WB.WHITE_PRIORITY,
              R.WHITE_BALANCE_R:'3',
              R.WHITE_BALANCE_B:'-5',
            #   R.KELVIN:'6500',
              R.HIGHLIGHTS:'0',
              R.SHADOWS:'-1',
              R.COLOR:'4',
              R.SHARPNESS:'-1',
              R.HIGH_ISONR:'-4',
              R.CLARITY:'-2',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)

    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    # (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    # assert act_count == 1 and act_value == exp_value

    # (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    # assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    # (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    # assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value


@pytest.mark.parametrize("cam", cameras)
def test_decimals_with_mid_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-mid.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'test-decimals.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'test-decimals',
              R.DYNAMIC_RANGE:DR.DR400,
              R.DRANGE_PRIORITY:DP.OFF,
              R.FILMSIMULATION:FS.CLASSIC_CHROME,
              R.BW_COLOR_WC:'-1',
              R.BW_COLOR_MC:'0',
              R.GRAIN_EFFECT:GR.WEAK_LARGE,
              R.CCR_EFFECT:CC.WEAK,
              R.CCRFX_BLUE:CC.STRONG,
              R.WHITE_BALANCE:WB.KELVIN,
              R.WHITE_BALANCE_R:'-1',
              R.WHITE_BALANCE_B:'1',
              R.KELVIN:'7010',
              R.HIGHLIGHTS:'0.5',
              R.SHADOWS:'-0.5',
              R.COLOR:'1',
              R.SHARPNESS:'-1',
              R.HIGH_ISONR:'-1',
              R.CLARITY:'1',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)

    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

@pytest.mark.parametrize("cam", cameras)
def test_max_with_min_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-min.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'test-max.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'test-max',
              R.DYNAMIC_RANGE:DR.DR400,
              R.DRANGE_PRIORITY:DP.OFF,
              R.FILMSIMULATION:FS.MONOCHROME,
              R.BW_COLOR_WC:'18',
              R.BW_COLOR_MC:'18',
              R.GRAIN_EFFECT:GR.STRONG_LARGE,
              R.CCR_EFFECT:CC.STRONG,
              R.CCRFX_BLUE:CC.STRONG,
              R.WHITE_BALANCE:WB.DAYLIGHT,
              R.WHITE_BALANCE_R:'9',
              R.WHITE_BALANCE_B:'9',
              R.KELVIN:'10000',
              R.HIGHLIGHTS:'4',
              R.SHADOWS:'4',
              R.COLOR:'4',
              R.SHARPNESS:'4',
              R.HIGH_ISONR:'4',
              R.CLARITY:'5'
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)
    
    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value


def get(tag, exp_lines, act_lines):
    """Boiler plate facade"""
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)

    return (exp_value, act_value, act_count)


def getProperty(tag, exp_lines, act_lines):
    """Boiler plate facade"""
    ((exp_count, exp_index, exp_value)) = search_propertyGroup(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_propertyGroup(tag, act_lines)

    return (exp_value, act_value, act_count)


@pytest.mark.parametrize("cam", cameras)
def test_mid_with_max_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-max.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'test-mid.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'test-mid',
              R.DYNAMIC_RANGE:DR.DR200,
              R.DRANGE_PRIORITY:DP.OFF,
              R.FILMSIMULATION:FS.ASTIA,
              R.BW_COLOR_MC:'0',
              R.GRAIN_EFFECT:GR.WEAK_SMALL,
              R.CCR_EFFECT:CC.WEAK,
              R.CCRFX_BLUE:CC.WEAK,
              R.WHITE_BALANCE:WB.KELVIN,
              R.KELVIN:'5500',
              R.WHITE_BALANCE_B:'0',
              R.HIGHLIGHTS:'0',
              R.SHADOWS:'0',
              R.COLOR:'0',
              R.SHARPNESS:'0',
              R.HIGH_ISONR:'0',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)

    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value


@pytest.mark.parametrize("cam", cameras)
def test_min_with_decimals_template(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-decimals.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'test-min.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'test-min',
              R.DYNAMIC_RANGE:DR.DR100,
              R.DRANGE_PRIORITY:DP.WEAK,
              R.FILMSIMULATION:FS.PROVIA,
              R.BW_COLOR_WC:'-18',
              R.BW_COLOR_MC:'-18',
              R.GRAIN_EFFECT:GR.OFF,
              R.CCR_EFFECT:CC.OFF,
              R.CCRFX_BLUE:CC.OFF,
              R.WHITE_BALANCE:WB.KELVIN,
              R.WHITE_BALANCE_R:'-9',
              R.WHITE_BALANCE_B:'-9',
              R.KELVIN:'2500',
              R.HIGHLIGHTS:'-2',
              R.SHADOWS:'-2',
              R.COLOR:'-4',
              R.SHARPNESS:'-4',
              R.HIGH_ISONR:'-4',
              R.CLARITY:'-5',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)
    assert tcam == cam
    
    (exp_value, act_value, act_count) = getProperty(C.LABEL, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.DYNAMIC_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value
    
    (exp_value, act_value, act_count) = get(C.WIDE_D_RANGE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.FILM_SIMULATION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.BLACK_IMAGE_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.MONOCHROMATIC_COLOR_RG, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    # Grain off, butcCustom cettings has 'random' size. Check not useful
    (exp_value, act_value, act_count) = get(C.GRAIN_EFFECT_SIZE, exp_lines, act_lines)
    assert act_count == 1 

    (exp_value, act_value, act_count) = get(C.CHROME_EFFECT, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR_CHROME_BLUE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WHITE_BALANCE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_R, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_SHIFT_B, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.WB_COLOR_TEMP, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.HIGHLIGHT_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHADOW_TONE, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.COLOR, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.SHARPNESS, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.NOIS_REDUCTION, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

    (exp_value, act_value, act_count) = get(C.CLARITY, exp_lines, act_lines)
    assert act_count == 1 and act_value == exp_value

