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
# Compares X Raw Studio file content with created content.
# #############################################################################

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

    tag = C.LABEL
    ((exp_count, exp_index, exp_value)) = search_propertyGroup(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_propertyGroup(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.DYNAMIC_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WIDE_D_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.FILM_SIMULATION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.BLACK_IMAGE_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.MONOCHROMATIC_COLOR_RG
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.GRAIN_EFFECT
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.GRAIN_EFFECT_SIZE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CHROME_EFFECT
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR_CHROME_BLUE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WHITE_BALANCE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_SHIFT_R
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_SHIFT_B
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_COLOR_TEMP
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value

    tag = C.HIGHLIGHT_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHADOW_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHARPNESS
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.NOIS_REDUCTION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CLARITY
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

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
              R.KELVIN:'10000',
              R.WHITE_BALANCE_R:'9',
              R.WHITE_BALANCE_B:'9',
              R.HIGHLIGHTS:'4',
              R.SHADOWS:'4',
              R.COLOR:'4',
              R.SHARPNESS:'4',
              R.HIGH_ISONR:'4',
              R.CLARITY:'5'
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)
    
    field = R.DYNAMIC_RANGE
    tag = C.DYNAMIC_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    
    field = R.DRANGE_PRIORITY
    tag = C.WIDE_D_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    field = R.FILMSIMULATION
    tag = C.FILM_SIMULATION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    tag = C.BLACK_IMAGE_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.MONOCHROMATIC_COLOR_RG
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag=C.GRAIN_EFFECT
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag=C.GRAIN_EFFECT_SIZE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CHROME_EFFECT
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR_CHROME_BLUE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WHITE_BALANCE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_SHIFT_R
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_SHIFT_B
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_COLOR_TEMP
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.HIGHLIGHT_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHADOW_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHARPNESS
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.NOIS_REDUCTION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CLARITY
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value


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

    
    field = R.DYNAMIC_RANGE
    tag = C.DYNAMIC_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    
    field = R.DRANGE_PRIORITY
    tag = C.WIDE_D_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    field = R.FILMSIMULATION
    tag = C.FILM_SIMULATION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    tag = C.BLACK_IMAGE_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value
    tag = C.MONOCHROMATIC_COLOR_RG
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CHROME_EFFECT
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR_CHROME_BLUE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WHITE_BALANCE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value

    tag = C.WB_SHIFT_R
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    tag = C.WB_SHIFT_B
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value
    tag = C.WB_COLOR_TEMP
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHADOW_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHARPNESS
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.NOIS_REDUCTION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CLARITY
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

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
              R.BW_COLOR_MC:'-18',
              R.WHITE_BALANCE:WB.KELVIN,
              R.WHITE_BALANCE_R:'-9',
              R.WHITE_BALANCE_B:'-9',
              R.GRAIN_EFFECT:GR.OFF,
              R.CCR_EFFECT:CC.OFF,
              R.WHITE_BALANCE:WB.KELVIN,
              R.KELVIN:'2500',
              R.HIGHLIGHTS:'-2',
              R.SHADOWS:'-2',
              R.COLOR:'-4',
              R.SHARPNESS:'-4',
              R.CLARITY:'-5',
              }

    act_lines = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)
    assert tcam == cam
    
    field = R.DYNAMIC_RANGE
    tag = C.DYNAMIC_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value
    
    field = R.DRANGE_PRIORITY
    tag = C.WIDE_D_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value

    field = R.FILMSIMULATION
    tag = C.FILM_SIMULATION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value

    tag = C.BLACK_IMAGE_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    tag = C.MONOCHROMATIC_COLOR_RG
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value
    tag = C.GRAIN_EFFECT
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR_CHROME_BLUE
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WHITE_BALANCE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.WB_SHIFT_R
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_value == exp_value

    tag = C.WB_SHIFT_B
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1

    tag = C.WB_COLOR_TEMP
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value
    tag = C.HIGHLIGHT_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHADOW_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.COLOR
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.SHARPNESS
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.NOIS_REDUCTION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value

    tag = C.CLARITY
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    ((act_count, act_index, act_value)) = search_tag(tag, act_lines)
    assert act_count == 1
    assert act_value == exp_value
