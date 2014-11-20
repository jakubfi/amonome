F_CPU=16000000UL
MCU=atmega168
PROGRAMMER_MCU=atmega168
PROJECTNAME=amonome-fw
PRJSRC=amonome-fw.c serial.c display.c keypad.c softboot.c
ANIM_A=anim_a.c
ANIM_B=anim_b.c
INC=
LIBS=
OPTLEVEL=s
AVRDUDE_PROGRAMMERID=arduino
AVRDUDE_OPTS=-b 115200
AVRDUDE_PORT_A=/dev/ttyUSB0
AVRDUDE_PORT_B=/dev/ttyUSB1
HEXFORMAT=ihex

# compiler
FLAGS=-I. $(INC) -g -mmcu=$(MCU) -O$(OPTLEVEL)  \
	-std=c99				\
	-DF_CPU=$(F_CPU)			\
	-fpack-struct -fshort-enums             \
	-ffunction-sections -fdata-sections	\
	-funsigned-bitfields -funsigned-char    \
	-Wall

CFLAGS=-Wa,-ahlms=$(firstword $(filter %.lst, $(<:.c=.lst)))

# c++ specific flags
CPPFLAGS=-fno-exceptions                \
	-Wa,-ahlms=$(firstword          \
	$(filter %.lst, $(<:.cpp=.lst)) \
	$(filter %.lst, $(<:.cc=.lst))  \
	$(filter %.lst, $(<:.C=.lst)))

# assembler
ASMFLAGS =-I. $(INC) -mmcu=$(MCU)        \
	-x assembler-with-cpp            \
	-Wa,-gstabs,-ahlms=$(firstword   \
		$(<:.S=.lst) $(<.s=.lst))


# linker
LDFLAGS=-mmcu=$(MCU) $(LIBS)

##### executables ####
CC=avr-gcc
CPP=avr-g++
OBJCOPY=avr-objcopy
OBJDUMP=avr-objdump
SIZE=avr-size
AVRDUDE=avrdude
REMOVE=rm -f

##### automatic target names ####
TRG_A=$(PROJECTNAME)-a.out
TRG_B=$(PROJECTNAME)-b.out
DUMPTRG_A=$(PROJECTNAME)-a.s
DUMPTRG_B=$(PROJECTNAME)-b.s

HEXROMTRG_A=$(PROJECTNAME)-a.hex 
HEXROMTRG_B=$(PROJECTNAME)-b.hex 
HEXTRG_A=$(HEXROMTRG_A) $(PROJECTNAME)-a.ee.hex
HEXTRG_B=$(HEXROMTRG_B) $(PROJECTNAME)-b.ee.hex

# Define all object files.

CPPFILES=$(filter %.cpp, $(PRJSRC))
CCFILES=$(filter %.cc, $(PRJSRC))
BIGCFILES=$(filter %.C, $(PRJSRC))
CFILES=$(filter %.c, $(PRJSRC))
ASMFILES=$(filter %.S, $(PRJSRC))

# List all common object files we need to create
OBJDEPS=$(CFILES:.c=.o) \
	$(CPPFILES:.cpp=.o)\
	$(BIGCFILES:.C=.o) \
	$(CCFILES:.cc=.o) \
	$(ASMFILES:.S=.o)

OBJ_A=$(ANIM_A:.c=.o)
OBJ_B=$(ANIM_B:.c=.o)

# Define all lst files.
LST=$(filter %.lst, $(OBJDEPS:.o=.lst) $(OBJ_A:.o=.lst) $(OBJ_B:.o=.lst))

# All the possible generated assembly 
# files (.s files)
GENASMFILES=$(filter %.s, $(OBJDEPS:.o=.s)) 


.SUFFIXES : .c .cc .cpp .C .o .out .s .S \
	.hex .ee.hex .h .hh .hpp


.PHONY: writeflash writeflash_a writeflash_b hex hex_a hex_b clean stats stats

# Make targets:
# all, disasm, stats, hex, writeflash/install, clean
all: $(TRG_A) $(TRG_B)

disasm: $(DUMPTRG_A) $(DUMPTRG_B) stats

stats: $(TRG_A) $(TRG_B)
	$(SIZE) $(TRG_A)
	$(SIZE) $(TRG_B)

hex: hex_a hex_b

hex_a: $(HEXTRG_A)
hex_b: $(HEXTRG_B)

writeflash_a: hex_a
	../tools/reboot.py a
	sleep 0.4
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMERID)	\
	-p $(PROGRAMMER_MCU) -e			\
	$(AVRDUDE_OPTS)				\
	-P $(AVRDUDE_PORT_A)			\
	-U flash:w:$(HEXROMTRG_A)

writeflash_b: hex_b
	../tools/reboot.py b
	sleep 0.4
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMERID)   \
	-p $(PROGRAMMER_MCU) -e                \
	$(AVRDUDE_OPTS)				\
	-P $(AVRDUDE_PORT_B)			\
	-U flash:w:$(HEXROMTRG_B)

install_a: writeflash_a
install_b: writeflash_b

install: writeflash_a writeflash_b

$(DUMPTRG_A): $(TRG_A) 
	$(OBJDUMP) -S  $< > $@

$(DUMPTRG_B): $(TRG_B) 
	$(OBJDUMP) -S  $< > $@

$(TRG_A): $(OBJDEPS) $(OBJ_A)
	$(CC) $(LDFLAGS) -Wl,-Map,$(TRG_A).map -o $(TRG_A) $(OBJDEPS) $(OBJ_A)

$(TRG_B): $(OBJDEPS) $(OBJ_B)
	$(CC) $(LDFLAGS) -Wl,-Map,$(TRG_B).map -o $(TRG_B) $(OBJDEPS) $(OBJ_B)


#### Generating assembly ####
# asm from C
%.s: %.c
	$(CC) -S $(FLAGS) $(CFLAGS) $< -o $@

# asm from (hand coded) asm
%.s: %.S
	$(CC) -S $(ASMFLAGS) $< > $@


# asm from C++
.cpp.s .cc.s .C.s :
	$(CPP) -S $(FLAGS) $(CPPFLAGS) $< -o $@



#### Generating object files ####
# object from C
.c.o: 
	$(CC) $(FLAGS) $(CFLAGS) -c $< -o $@


# object from C++ (.cc, .cpp, .C files)
.cc.o .cpp.o .C.o :
	$(CPP) $(FLAGS) $(CPPFLAGS) -c $< -o $@

# object from asm
.S.o :
	$(CC) $(ASMFLAGS) -c $< -o $@


#### Generating hex files ####
# hex files from elf
#####  Generating a gdb initialisation file    #####
.out.hex:
	$(OBJCOPY) -j .text                    \
		-j .data                       \
		-O $(HEXFORMAT) $< $@

.out.ee.hex:
	$(OBJCOPY) -j .eeprom                  \
		--change-section-lma .eeprom=0 \
		-O $(HEXFORMAT) $< $@


#### Cleanup ####
clean:
	$(REMOVE) $(TRG_A) $(TRG_A).map $(DUMPTRG_A)
	$(REMOVE) $(TRG_B) $(TRG_B).map $(DUMPTRG_B)
	$(REMOVE) $(OBJDEPS) $(OBJ_A) $(OBJ_B)
	$(REMOVE) $(LST) $(GDBINITFILE)
	$(REMOVE) $(GENASMFILES)
	$(REMOVE) $(HEXTRG_A) $(HEXTRG_B)

