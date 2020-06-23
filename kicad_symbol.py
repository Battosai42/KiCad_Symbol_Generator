#!/usr/bin/python
#  -*- coding: utf-8 -*-

""" KiCad 5 Symbol Format

This Class can be used to generate KiCad symbols and implements the file format in an easy way.

Available Functions:    createComponent()
                        createAlias()
                        createFields()
                        createPin()
                        createRectangle()
                        createPolygon()
                        createCircle()
                        createArc()
"""

__author__ = 'Samuel Blatter'
__maintainer__ = 'Samuel Blatter'
__email__ = 'git.b42@gmail.com'
__credits__ = ''
__version__ = '0.0.1'
__status__ = 'Developement'

import logging


class KiCadPin:
    """
    KiCadPin implements a basic pin class adhering to the KiCad symbol file definitions
    """
    logger = logging.getLogger(__name__)
    _name = ''
    _number = None
    _pos = [0, 0]
    _length = None
    _orientation = None
    _snum = None
    _snom = None
    _unit = None
    _convert = None
    _etype = None
    _shape = None

    def __init__(self, name='default', number=0, posx=0, posy=0, length=100, orientation='L', snum=50,
               snom=50, unit=0, convert=1, etype='I', shape=''):
        self.setPin(name=name, number=number, posx=posx, posy=posy, length=length, orientation=orientation,
                          snum=snum, snom=snom, unit=unit, convert=convert, etype=etype, shape=shape)

    def setPin(self, name='default', number=0, posx=0, posy=0, length=100, orientation='L', snum=50,
               snom=50, unit=0, convert=1, etype='I', shape=''):
        """
        Manual Pin generation

        :param name:
        :param number:
        :param posx:
        :param posy:
        :param length:
        :param orientation:
        :param snum:
        :param snom:
        :param unit:
        :param convert:
        :param etype:
        :param shape:
        :return:
        """
        self._name = name
        self._number = number
        self._pos = [posx, posy]
        self._length = length
        self._orientation = orientation
        self._snum = snum
        self._snom = snom
        self._unit = unit
        self._convert = convert
        self._etype = etype
        self._shape = shape
        self.logger.info(' Created Pin: {}'.format(self.getPin()))

    def updatePin(self, param='', value=None):
        """
        Get pin parameter(s)

        :param param: "name, number, posx, posy, length, orientation, snum, snom, unit, convert, etype, shape"
        :return:
        """
        if param.lower() == 'name':
            self._name = value
        elif param.lower() == 'number':
            self._number = value
        elif param.lower() == 'posx':
            self._pos[0] = value
        elif param.lower() == 'posy':
            self._pos[1] = value
        elif param.lower() == 'length':
            self._length = value
        elif param.lower() == 'orientation':
            self._orientation = value
        elif param.lower() == 'snum':
            self._snum = value
        elif param.lower() == 'snom':
            self._snom = value
        elif param.lower() == 'unit':
            self._unit = value
        elif param.lower() == 'convert':
            self._convert = value
        elif param.lower() == 'etype':
            self._etype = value
        elif param.lower() == 'shape':
            self._shape = value
        self.logger.info('updated parameter "{}"= {}'.format(param, value))

    def getPin(self, param=''):
        """
        Get pin parameter(s)

        :param param: "name, number, posx, posy, length, orientation, snum, snom, unit, convert, etype, shape"
        :return:
        """
        if param.lower() == 'name':
            return self._name
        elif param.lower() == 'number':
            return self._number
        elif param.lower() == 'posx':
            return self._pos[0]
        elif param.lower() == 'posy':
            return self._pos[1]
        elif param.lower() == 'length':
            return self._length
        elif param.lower() == 'orientation':
            return self._orientation
        elif param.lower() == 'snum':
            return self._snum
        elif param.lower() == 'snom':
            return self._snom
        elif param.lower() == 'unit':
            return self._unit
        elif param.lower() == 'convert':
            return self._convert
        elif param.lower() == 'etype':
            return self._etype
        elif param.lower() == 'shape':
            return self._shape
        else:
            pin = 'X {} {} {} {} {} {} {} {} {} {} {} {}'.format(self._name, self._number, self._pos[0], self._pos[1],
                                                                 self._length, self._orientation, self._snum,
                                                                 self._snom, self._unit, self._convert, self._etype,
                                                                 self._shape)
            return pin


class KiCadSymbol():
    logger = logging.getLogger(__name__)

    def __init__(self, name='default'):
        self.resetComponent()
        self.name = name

    def resetComponent(self):
        self.name = ''
        self.header = 'EESchema-LIBRARY Version 2.4'
        self.component = []
        self.alias = ''
        self.fields = []
        self.geometry = []
        self.pins = []
        self.footprints = []

    # Create Component and Pins
    def createComponent(self, name='Default', reference='U', unused=0, text_offset=5, draw_pinnumber='Y',
                        draw_pinname='Y', unit_count=1, units_locked='L', option_flag='N'):
        """
        Format: "DEF name reference unused text_offset draw_pinnumber draw_pinname unit_count units_locked option_flag"

        :param name: component name in library (74LS02 ...)
        :param reference: Reference ( U, R, IC .., which become U3, U8, R1, R45, IC4...)
        :param unused: 0 (reserved)
        :param text_offset: offset for pin name position
        :param draw_pinnumber: Y (display pin number) ou N (do not display pin number).
        :param draw_pinname: Y (display pin name) ou N (do not display pin name).
        :param unit_count: Number of part ( or section) in a component package.
        :param units_locked: L (units are not identical and cannot be swapped) or F (units are identical and therefore 
                             can be swapped) (Used only if unit_count > 1)
        :param option_flag: N (normal) or P (component type "power")
        :return: 
        """
        comp = 'DEF {} {} {} {} {} {} {} {} {}'.format(name, reference, unused, text_offset, draw_pinnumber,
                                                                 draw_pinname, unit_count, units_locked, option_flag)
        self.logger.info(' Created Component: {}'.format(comp))
        self.component.append('#')
        self.component.append('# {}'.format(name))
        self.component.append('#')
        self.component.append(comp)

    def createAlias(self, alias=[]):
        """
        Format: "ALIAS name1 name2 name3..."

        :param alias: [name1, name2, name3, ...]
        :return:
        """
        if alias != False:
            alia = 'ALIAS '
            for i in alias:
                alia = '{} {}'.format(alia, i)
            self.alias = alia
            self.logger.info(' Created Alias: {}'.format(self.alias))

    def createFields(self, n=0, text='', posx=0, posy=0, dimension=50, orientation='L', visibility='V', hjustify='L',
                     vjustify='C', style='', name=''):
        """
        Format: F n “text” posx posy dimension orientation visibility hjustify vjustify/italic/bold “name”

        Notes:
        - The F1 field is the default component value and the component name in library. So the F1 field text should be
        the same as the name.
        - F0 is the reference prefix. If the prefix starts b # (like #U) the component is not output to netlist or Bill
        Of Material. This is a “virtual” component. Mainly power symbols must have the prefix starting by #.


        ;param n: field number :    • reference = 0.
                                    • value = 1.
                                    • Pcb FootPrint = 2.
                                    • User doc link = 3. At present time: not used
                                    • n = 4..11 = fields 1 to 8 (since January 2009 more than 8 field allowed, so n can be > 11.
        :param text: text (delimited by double quotes)
        :param posx: position X
        :param posy: position Y
        :param dimension: dimension (default = 50)
        :param orientation: rientation = H (horizontal) or V (vertical).
        :param visibility: Visibility = V (visible) or I (invisible)
        :param hjustify: hjustify = L R C B or T (L= left, R = Right, C = centre, B = bottom, T = Top)
        :param vjustify: vjustify = L R C B or T (L= left, R = Right, C = centre, B = bottom, T = Top)
        ;param style:   • Italic: I or N ( since January 2009)
                        • Bold: B or N ( since January 2009)
        :param name: Name of the field (delimited by double quotes) (only if it is not the default name)
        :return:
        """
        field = 'F{} {} {} {} {} {} {} {} {}{}{}'.format(n, text, posx, posy, dimension, orientation, visibility,
                                                          hjustify, vjustify, style, name)
        self.logger.info(' Created field: {}'.format(field))
        self.fields.append(field)

    def createPin(self, name='default', number=0, posx=0, posy=0, length=100, orientation='L', snum=50, snom=50,
               unit=0, convert=1, etype='I', shape=''):
        """
        Format: "X name number posx posy length orientation snum snom unit convert Etype [shape]"

        :param name: name (without space) of the pin. if ~: no name
        :param number: n pin number (4 characters maximum).
        :param posx:
        :param posy:
        :param length: pin length.
        :param orientation: U (up) D (down) R (right) L (left).
        :param Snum: pin number text size.
        :param Snom: pin name text size.
        :param unit: 0 if common to all parts. If not, number of the part (1. .n).
        :param convert: 0 if common to the representations, if not 1 or 2.
        :param etype: electric type (1 character) [INPUT I, OUTPUT O, BIDI B, TRISTATE T, PASSIVE P, UNSPECIFIED U,
                      POWER INPUT W, POWER OUTPUT w, OPEN COLLECTOR C, OPEN EMITTER E, NOT CONNECTED N]
        :param shape: if present: pin shape (clock, inversion...). (If invisible pin, the shape identifier starts by N)
                      followed by: [Line None (default), Inverted I, Clock C, Inverted clock CI, Input low L,
                      Clock low CL, Output low V, Falling edge clock F, Non Logic]
        :return:
        """
        pin = KiCadPin(name, number, posx, posy, length, orientation, snum, snom, unit, convert, etype, shape)
        self.pins.append(pin)

    def createFootprint(self, footprint=None):
        """
        Format: footprint="SOIC*3.9x4.9mm*P1.27mm*"

        :param footprints: [footprint1, footprint2]
        :return:
        """
        if footprint is not None:
            self.footprints.append(footprint)
        self.logger.info(' Created Footprint: {}'.format(footprint))

    # Create Geometries
    def createRectangle(self, startx=0, starty=0, endx=10, endy=10, unit=1, convert=0, thickness=0, cc='N'):
        """
        Format: S startx starty endx endy unit convert thickness cc

        :param startx: start coordinates in X
        :param starty: start coordinates in Y
        :param endx: end coordinates in X
        :param endy: end coordinates in Y
        :param unit: unit = 0 if common to the parts; if not, number of part (1. .n)
        :param convert: convert = 0if common to all parts. If not, number of the part (1. .n)
        :param thickness: thickness = thickness of the outline
        :param cc: cc = N F or F ( F = filled Rectangle,; f = . filled Rectangle, N = transparent background)
        :return:
        """
        rect = 'S {} {} {} {} {} {} {} {}'.format(startx, starty, endx, endy, unit, convert, thickness, cc)
        self.logger.info(' Created Geometry: {}'.format(rect))
        self.geometry.append(rect)

    def createPolygon(self, parts=1, convert=0, thickness=0, x=[], y=[], cc='N'):
        """
        Format : P Nb parts convert thickness x0 y0 x1 y1 xi yi cc

        :param Nb: Number of points
        :param parts: 0 if common to the parts; if not, number of part (1. .n).
        :param convert: 0 if common to the 2 representations, if not 1 or 2.
        :param thickness: line thickness.
        :param x: x coordinates [x1, x2, x3, ...]
        :param y: y coordinates [y1, y2, y3, ...]
        :param cc: N F or F ( F = filled polygon; f = . filled polygon, N = transparent background)
        :return:
        """
        coordinates = ''
        for i in range(len(x)):
            coordinates = '{} {} {}'.format(coordinates, x[i], y[i])
        poly = 'P {} {} {} {}{} {}'.format(len(x), parts, convert, thickness, coordinates, cc)
        self.logger.info(' Created Polygon: {}'.format(poly))
        self.geometry.append(poly)

    def createCircle(self, posx=0, posy=0, radius=1, unit=1, convert=0, thickness=0, cc='N'):
        """
        Format: C posx posy radius unit convert thickness cc

        :param posx: circle center position
        :param posy: circle center position
        :param radius:
        :param unit: 0 if common to the parts; if not, number of part (1. .n).
        :param convert: 0 if common to all parts. If not, number of the part (1. .n).
        :param thickness: thickness of the outline.
        :param cc: N F or F ( F = filled circle,; f = . filled circle, N = transparent background)
        :return:
        """
        cir = 'C {} {} {} {} {} {} {}'.format(posx, posy, radius, unit, convert, thickness, cc)
        self.logger.info(' Created Circle: {}'.format(cir))
        self.geometry.append(cir)

    def createArc(self, posx=0, posy=0, radius=1, start=0, end=90, part=1, convert=0, thickness=0, cc='N',
                  start_pointX=0, start_pointY=0, end_pointX=1, end_pointY=1):
        """
        Format: A posx posy radius start end part convert thickness cc start_pointX start_pointY end_pointX end_pointY.

        :param posx: arc center position
        :param posy: arc center position
        :param radius:
        :param start: angle of the starting point (in 0,1 degrees).
        :param end: angle of the end point (in 0,1 degrees).
        :param part: 0 if common to all parts; if not, number of the part (1. .n).
        :param convert: 0 if common to the representations, if not 1 or 2.
        :param thickness: thickness of the outline or 0 to use the default line thickness.
        :param cc: N F or F ( F = filled arc,; f = . filled arc, N = transparent background)
        :param start_pointX: coordinate of the starting point (role similar to start)
        :param start_pointY: coordinate of the starting point (role similar to start)
        :param end_pointX: coordinate of the end point (role similar to start)
        :param end_pointY: coordinate of the end point (role similar to start)
        :return:
        """
        arc = 'A {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(posx, posy, radius, start, end, part, convert,
                                                                thickness, cc, start_pointX, start_pointY, end_pointX,
                                                                end_pointY)
        self.logger.info(' Created Arc: {}'.format(arc))
        self.geometry.append(arc)

    # Symbol operations
    def writeSymbol(self, library=None, mode='a'):
        """

        :param path: file path to library location
        :param library: library name "library.lib"
        :param mode:    r+: Opens a file for reading and writing, placing the pointer at the beginning of the file
                        w+: Opens a file for writing and reading
                        a: Opens a file for appending new information to it. The pointer is placed at the end of the
                        file. A new file is created if one with the same name doesn't exist.
        :return:
        """
        try:
            symbol = open(file=library, mode=mode)
            symbol.write(self.header)
            symbol.write('\n')
            for line in self.component:
                symbol.write(line)
                symbol.write('\n')
            for line in self.fields:
                symbol.write(line)
                symbol.write('\n')
            symbol.write('$FPLIST\n')
            for line in self.footprints:
                symbol.write(line)
                symbol.write('\n')
            symbol.write('$ENDFPLIST\n')
            symbol.write('DRAW\n')
            for line in self.geometry:
                symbol.write(line)
                symbol.write('\n')
            for line in self.pins:
                symbol.write(line.getPin())
                symbol.write('\n')
            symbol.write('ENDDRAW\n')
            symbol.write('ENDDEF\n')
            self.logger.info(' Finished writing symbol to library')
            symbol.close()
        except Exception as e:
            print(' Could not write to symbol to library: {}'.format(e))

    def readSymbol(self, library=None, component=None):
        """

        :param path:
        :param library:
        :param component:
        :return:
        """
        # make sure the component is reset
        self.resetComponent()
        self.name = component

        try:
            symbol = open(file='{}'.format(library), mode='r')
            for line in symbol:
                if 'DEF {}'.format(component.upper()) in line.upper():
                    comp = line.upper().rstrip().split(' ')
                    self.createComponent(name=comp[1], reference=comp[2], unused=comp[3], text_offset=comp[4],
                                          draw_pinnumber=comp[5], draw_pinname=comp[6], unit_count=comp[7],
                                          units_locked=comp[8], option_flag=comp[9])
                    self.logger.info(' Component found: {}'.format(self.name))
                elif line[0].upper() == 'F':
                    field = line.rstrip()[1:].split(' ')
                    self.createFields(n=field[0], text=field[1], posx=field[2], posy=field[3], dimension=field[4],
                                      orientation=field[5], visibility=field[6], hjustify=field[7], vjustify=field[8][0],
                                      style=field[8][1], name=field[8][2])
                elif 'ALIAS' in line:
                    self.alias = line
                elif line[0] == ' ':
                    self.createFootprint(footprint=line.rstrip())
                elif line[0].upper() == 'P':
                    poly = line.rstrip()[2:].split(' ')
                    x=[]
                    y=[]
                    for i in range(4, len(poly)-1, 2):
                        x.append(poly[i])
                        y.append(poly[i+1])
                    self.createPolygon(parts=poly[1], convert=poly[2], thickness=poly[3], x=x, y=y, cc=poly[-1])
                elif line[0].upper() == 'S':
                    rect = line.upper().rstrip()[1:].split(' ')
                    self.createRectangle(startx=rect[0], starty=rect[1], endx=rect[2], endy=rect[3], unit=rect[4],
                                         convert=rect[5], thickness=rect[6], cc=rect[7])
                elif line[0].upper() == 'C':
                    cir = line.upper().rstrip()[2:].split(' ')
                    self.createCircle(posx=cir[0], posy=cir[1], radius=cir[2], unit=cir[3], convert=cir[4],
                                      thickness=cir[5], cc=cir[6])
                elif line[0].upper() == 'A':
                    arc = line.upper().rstrip()[1:].split(' ')
                    self.createArc(posx=arc[0], posy=arc[1], radius=arc[2], start=arc[3], end=arc[4], part=arc[5],
                                   convert=arc[6], thickness=arc[7], cc=arc[8], start_pointX=arc[9], start_pointY=arc[10],
                                   end_pointX=arc[11], end_pointY=arc[12])
                elif line[0].upper() == 'X':
                    pin = line.rstrip().split(' ')
                    try:
                        shape = pin[12]
                    except:
                        shape = ''
                    self.createPin(name=pin[1], number=pin[2], posx=pin[3], posy=pin[4], length=pin[5],
                                              orientation=pin[6], snum=pin[7], snom=pin[8], unit=pin[9],
                                              convert=pin[10], etype=pin[11], shape=shape)
                elif 'ENDDEF' in line.upper():
                    break
            symbol.close()

        except Exception as e:
            print('Reading symbol failed: {}'.format(e))


class SymbolTools:
    """
    This class contains helper tools to manipulate already existing symbols. Currently the following are implemented:

        Tools:
        - compareSymbols: compare and and fix differences in two symbols
    """
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.logger.info('Symbol Tools')

    def compareSymbols(self, libraryA=None, libraryB=None, componentA=None, componentB=None, param='number', fix=None):
        """
        Compare two symbols with each other

        :param libraryA: full path to library
        :param libraryB: full path to library (equal to libraryA A if omitted)
        :param componentA: name of component A
        :param componentB: name of component A (equal to componentA if omitted)
        :param param: [name, number, posx, posy, length, orientation, snum, snom, unit, convert, etype, shape]
        :param fix: if True the script will fix the component in libraryB
        :return:
        """
        if componentB == None:
            componentB = componentA
        if libraryB == None:
            libraryB = libraryA

        error = False
        symbolA = KiCadSymbol()
        symbolB = KiCadSymbol()
        symbolA.readSymbol(library=libraryA, component=componentA)
        symbolB.readSymbol(library=libraryB, component=componentB)

        pins = range(len(symbolA.pins))

        for i in pins:
            name = symbolA.pins[i].getPin(param='name')
            for i in pins:
                if name == symbolB.pins[i].getPin(param='name'):
                    nA = symbolA.pins[i].getPin(param=param)
                    nB = symbolB.pins[i].getPin(param=param)
                    if nA != nB:
                        print('Mismatch Found! Pad: {}, pin Number {} vs {}'.format(name, nA, nB))
                        if fix is True:
                            error = True
                            symbolB.pins[i].updatePin(param='number', value=nA)
                            print('fixed pad {}: {}'.format(param, symbolB.pins[i].getPin(param=param)))
                        break

        if fix is True and error is True:
            symbolB.writeSymbol(library=libraryB, mode='w')
            print('saved fixed library to {}'.format(libraryB))


def example():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    sym = KiCadSymbol()
    sym.createPin(name='test')
    sym.createPin(name='test2')
    sym.createAlias(alias=['alias1', 'alias2'])
    sym.createPolygon(x=[1,2,3,4], y=[4,3,2,1])
    sym.createCircle()
    sym.createArc()
    sym.createComponent()

def exampleRead():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    library = 'C:/Program Files/KiCad/share/kicad/library/Amplifier_Operational.lib'
    component = 'AD8015'
    sym = KiCadSymbol()
    sym.readSymbol(library=library, component=component)
    print(sym.pins[1].getPin())

    sym.writeSymbol(path='C:/Users/Battosai/Downloads', library='test.lib', mode='w')

def examplepin():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    test = 'X Vbyp 4 0 -300 150 U 50 50 1 1 I'.split(' ')
    #print(test)

    pin = KiCadPin(name='testpin2', number=2)
    pin2 = KiCadPin(test)
    print(pin2.getPin())

def compareSym():
    library = 'C:/Program Files/KiCad/share/kicad/library/Amplifier_Operational.lib'
    library2 = 'C:/Users/Battosai/Downloads/test.lib'
    component = 'AD8015'

    tool = SymbolTools()
    tool.compareSymbols(libraryA=library, libraryB=library2, componentA=component, fix=True)

if __name__ == "__main__":
    compareSym()