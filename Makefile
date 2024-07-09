CPP=g++
CARGS=-std=c++17 -O0 -g3 -m64 -Werror -Wall
BRKGAINC=-I ../nsbrkga/nsbrkga
BOOSTINC=-I /opt/boost/include -L /opt/boost/lib -lboost_serialization
PAGMOINC=-I /opt/pagmo/include -L /opt/pagmo/lib -Wl,-R/opt/pagmo/lib -lpagmo -ltbb -pthread
INC=-I src $(BRKGAINC) $(BOOSTINC) $(PAGMOINC)
MKDIR=mkdir -p
RM=rm -rf
SRC=$(PWD)/src
BIN=$(PWD)/bin

clean:
	@echo "--> Cleaning compiled..."
	$(RM) $(BIN)
	@echo

$(BIN)/%.o: $(SRC)/%.cpp
	@echo "--> Compiling $<..."
	$(MKDIR) $(@D)
	$(CPP) $(CARGS) -c $< -o $@ $(INC)
	@echo

$(BIN)/test/nsga2_solver_test : $(BIN)/solver/solver.o \
                                $(BIN)/solver/nsga2/nsga2_solver.o \
                                $(BIN)/test/nsga2_solver_test.o 
	@echo "--> Linking objects..." 
	$(CPP) -o $@ $^ $(CARGS) $(INC)
	@echo
	@echo "--> Running test..."
	$(BIN)/test/nsga2_solver_test
	@echo

nsga2_solver_test : clean $(BIN)/test/nsga2_solver_test

$(BIN)/test/nspso_solver_test : $(BIN)/solver/solver.o \
                                $(BIN)/solver/nspso/nspso_solver.o \
                                $(BIN)/test/nspso_solver_test.o 
	@echo "--> Linking objects..." 
	$(CPP) -o $@ $^ $(CARGS) $(INC)
	@echo
	@echo "--> Running test..."
	$(BIN)/test/nspso_solver_test
	@echo

nspso_solver_test : clean $(BIN)/test/nspso_solver_test

$(BIN)/test/moead_solver_test : $(BIN)/solver/solver.o \
                                $(BIN)/solver/moead/moead_solver.o \
                                $(BIN)/test/moead_solver_test.o 
	@echo "--> Linking objects..." 
	$(CPP) -o $@ $^ $(CARGS) $(INC)
	@echo
	@echo "--> Running test..."
	$(BIN)/test/moead_solver_test
	@echo

moead_solver_test : clean $(BIN)/test/moead_solver_test

tests: nsga2_solver_test \
	   nspso_solver_test \
	   moead_solver_test \

all: tests
