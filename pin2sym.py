#!/usr/bin/python
#  -*- coding: utf-8 -*-

""" Generate a simple kicad symbol from an input netlist

    usage:
    pin2sym.py -i <inputfile> -o <output file> -p <package>

    supported input formats:
        input [3:0] binary_in  ;
        input  enable ;
        output [15:0] decoder_out ;
        inout [15:0] decoder_out ;

"""

__author__ = 'Samuel Blatter'
__maintainer__ = 'Samuel Blatter'
__email__ = 'git.b42@gmail.com'
__credits__ = ''
__version__ = '0.0.1'
__status__ = 'Developement'

# Imports
import sys
import getopt
import logging


def main():
    logger = logging.getLogger(__name__)
    outfile = None
    infile = None
    package = 'noname'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:p:", ["ifile=", "ofile=", "package="])
    except getopt.GetoptError as err:
        print('test.py -i <input file> -o <outfile> -p <package>')
        print(err)
        sys.exit(2)
    for opt, arg in opts:

        if opt in ('-h', "--help"):
            print("\nUsage of this Script:\n\n")
            print('pinlist2symbol.py -i <input file> -o <outfile> -p <package>\n')
            print('<input file> has to be the path including the file name (expected format: .csv)')
            print('<outfile> has to be the path including the file name (expected format: .png)')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt in ("-o", "--ofile"):
            outfile = arg
        elif opt in ("-p", "--package"):
            package = arg
        else:
            assert False, "unhandled option"

    print("\n")
    print("using the following settings:")
    print('    input file:  {}'.format(infile))
    print('    output file: {}'.format(outfile))
    print('    Package:     {}'.format(package))
    print('\n')

# start of symbol generation
    device_name = 'test'
    number_of_parts = 1
    text_size = 50
    show_pin_numbers = 'Y'
    show_pin_names = 'Y'
    xoffset = 0
    yoffset = 0
    pins = []
    orientation = 'R'
    direction = []

    with open(infile, 'r') as pinlist:
        while True:
            line = ' '.join(pinlist.readline().split()).replace(';', '').split(' ')
            if len(line) == 2:
                dir = line[0]
                bus = ''
                pin = line[1]
            elif len(line) == 3:
                dir = line[0]
                bus = line[1]
                pin = line[2]
            else:
                break

            if bus == '':
                pins.append(pin)
                if dir.lower() == 'input':
                    direction.append('I')
                elif dir.lower() == 'output':
                    direction.append('O')
                elif dir.lower() == 'inout':
                    direction.append('B')
                else:
                    print('invalid direction')
            else:
                n = int(bus.split(':')[0].replace('[', ''))+1
                for p in range(n):
                    pins.append('{}{}'.format(pin, p))
                    if dir.lower() == 'input':
                        direction.append('I')
                    elif dir.lower() == 'output':
                        direction.append('O')
                    elif dir.lower() == 'inout':
                        direction.append('B')
                    else:
                        print('invalid direction')

    with open(outfile, 'w') as symbol:
        # write header
        symbol.write('EESchema-LIBRARY Version 2.4\n')
        symbol.write('#encoding utf-8\n')
        symbol.write('#\n')
        symbol.write('# {}\n'.format(device_name))
        symbol.write('#\n')

        # write definitions
        symbol.write('DEF {} X 0 40 {} {} {} F N\n'.format(device_name, show_pin_names, show_pin_names, number_of_parts))
        # write the symbol prefix
        symbol.write('F0 "X" {} {} {} H V R CNN\n'.format(xoffset+1500, yoffset+50, text_size))
        # write the symbol name
        symbol.write('F1 "{}" {} {} {} H V L CNN\n'.format(device_name, xoffset, yoffset+50, text_size))

        # footprint
        symbol.write('$FPLIST\n')
        symbol.write(' {}\n'.format(package))
        symbol.write('$ENDFPLIST\n')

        # draw symbol
        symbol.write('DRAW\n')

        # Pins
        yoffsetL = yoffset-100
        yoffsetR = yoffset-100
        for i in range(len(pins)):
            if direction[i] == 'I' or direction[i] == 'B':
                symbol.write('X {} {} {} {} 150 {} {} {} 1 1 {}\n'.format(pins[i], i, xoffset-150, yoffsetR, 'R', text_size, text_size, direction[i]))
                yoffsetR += -100
            elif direction[i] == 'O':
                symbol.write('X {} {} {} {} 150 {} {} {} 1 1 {}\n'.format(pins[i], i, xoffset+1650, yoffsetL, 'L', text_size, text_size, direction[i]))
                yoffsetL += -100

        # draw square
        symbol.write('S 0 0 1500 {} 0 0 10 f\n'.format(min([yoffsetL, yoffsetR])))

        # write foot
        symbol.write('ENDDRAW\n')
        symbol.write('ENDDEF\n')
        symbol.write('#\n')
        symbol.write('#End Library\n')

    print('done generating symbol')


if __name__ == "__main__":
    main()
