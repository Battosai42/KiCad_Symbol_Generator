#!/usr/bin/python3

inp = 'C:/Users/sbla/Downloads/test.v'
outp= 'C:/Users/sbla/Downloads/test1.lib'

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

with open(inp, 'r') as pinlist:
    while True:
        line = pinlist.readline().split(' ')
        if line == ['']:
            break
        else:
            dir = line[0]
            bus = line[1]
            pin = line[2]

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

with open(outp, 'w') as symbol:
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
    symbol.write('TSSOP - 16*\n')
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
