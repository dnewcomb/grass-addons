MODULE_TOPDIR = ../..

PGM = r.hydrobasin

LIBES = $(RASTERLIB) $(VECTORLIB) $(DBMILIB) $(GISLIB) $(MATHLIB)
DEPENDENCIES = $(RASTERDEP) $(VECTORDEP) $(DBMIDEP) $(GISDEP)
EXTRA_LIBS = $(OPENMP_LIBPATH) $(OPENMP_LIB)
EXTRA_INC = $(VECT_INC) $(OPENMP_INCPATH)
EXTRA_CFLAGS = $(VECT_CFLAGS) $(OPENMP_CFLAGS)

include $(MODULE_TOPDIR)/include/Make/Module.make

default: cmd
