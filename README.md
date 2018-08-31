# KiCad_Symbol_Generator

This script is intended to read a file containing a verilog style pinlist and automatically generate a Kicad compatible symbol from it. 

## Task List
- [x] basic symbol generation
- [x] reading of basic input file (see example)
- [ ] verilog file as input
- [ ] spice file as input

## Example input file:
```
input [3:0] binary_in  ;
input  enable ;
output [15:0] decoder_out ;
inout [15:0] decoder_out ;
```

Currently tested on KiCad 5.0
