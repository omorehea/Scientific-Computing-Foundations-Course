FC = gfortran
FFLAGS = -Wall -Wextra -Wimplicit-interface -Wno-surprising -fPIC -fmax-errors=1 -g -fcheck=all -fbacktrace -fdefault-real-8 -fdefault-double-8 -J ./obj

ODIR=obj
_OBJ = utility.o setup_module.o leapfrog_module.o fput.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

fput: $(OBJ)
	$(FC) -o $@ $^ $(FFlAGS)

$(ODIR)/%.o: %.f90
	$(FC) -c -o $@ $< $(FFLAGS)

.PHONY: clean

clean:
	rm -f fput obj/* *~

