# Simple tool to convert recipies file from a properitary csv to the reciper's csv file format. Can be used as template for other converter.
# The created csv file is ready to import in recipies.py
# Import CSV may not have spaces before or after the column values.
import argparse
import csv
import constants.recipefields as R
import constants.csvfields as CSV

args = None

rfields = [
    R.NAME,
    R.PUBLISHER,
    R.FILMSIMULATION,
    R.BW_FILTER,
    R.BW_COLOR_WC,
    R.BW_COLOR_MC,
    R.GRAIN_EFFECT,
    R.CCR_EFFECT,
    R.CCRFX_BLUE,
    R.WHITE_BALANCE,
    R.KELVIN,
    R.WHITE_BALANCE_R,
    R.WHITE_BALANCE_B,
    R.DYNAMIC_RANGE,
    R.DRANGE_PRIORITY,
    R.HIGHLIGHTS,
    R.SHADOWS,
    R.SHARPNESS,
    R.COLOR,
    R.HIGH_ISONR,
    R.CLARITY,
    R.ISO_MIN,
    R.ISO_MAX,
    R.ISO,
    R.XTRANS_VERSION,
]
cfields = [
    CSV.NAME,
    CSV.PUBLISHER,
    CSV.FILMSIMULATION,
    CSV.BW_COLOR_WC,
    CSV.BW_COLOR_MC,
    CSV.GRAIN_EFFECT,
    CSV.CCR_EFFECT,
    CSV.CCRFX_BLUE,
    CSV.WHITE_BALANCE,
    CSV.KELVIN,
    CSV.WHITE_BALANCE_R,
    CSV.WHITE_BALANCE_B,
    CSV.DYNAMIC_RANGE,
    CSV.DRANGE_PRIORITY,
    CSV.HIGHLIGHTS,
    CSV.SHADOWS,
    CSV.SHARPNESS,
    CSV.COLOR,
    CSV.HIGH_ISONR,
    CSV.CLARITY,
    CSV.ISO_MIN,
    CSV.ISO_MAX,
    CSV.XTRANS_VERSION,
]

def main():

    all = []

    with open(args.input, newline='') as rfile:
        with open('recipies.csv', 'w', newline='') as wfile:
            spamreader = csv.DictReader(rfile, delimiter=',', quotechar='"')
            spamwriter = csv.writer(wfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
            
            spamwriter.writerow(cfields)
            for row in spamreader:
                print(row)
                values = []
                for f in cfields:
                    values.append(row[f])
                spamwriter.writerow(values)
            

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, nargs=1, default='import/X-Recipies.csv',
                        help='Input CSV file (Default: %(default)s).')

    parser.add_argument('-o', '--output', type=str, nargs=1, default='recipies.csv',
                        help='Output CSV file (Default: %(default)s).')

    args = parser.parse_args()


def err(message):
    """Print message an exit with '1'"""
    print(f"ERROR {message}")
    exit(1)

if __name__ == '__main__':
    parse_args()
    main()
