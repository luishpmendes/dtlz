#pragma once

#include "solver/solver.hpp"

namespace dtlz {
/*******************************************************************
 * The NSGA2_Solver represents a solver for the DTLZ test functions
 * using the Non-Dominated Sorting Genetic Algorithm II.
 *******************************************************************/
class NSGA2_Solver : public Solver {
    public:

    /************************************
     * Crossover probability.
     ************************************/
    double crossover_probability = 0.95;

    /**************************************
     * Distribution index for crossover.
     **************************************/
    double crossover_distribution = 10.00;

    /***********************************
     * Mutation probability.
     ***********************************/
    double mutation_probability = 0.01;

    /*************************************
     * Distribution index for mutation.
     *************************************/
    double mutation_distribution = 50.00;

    /*************************************************************
     * Constructs a new solver.
     *
     * @param dtlz the id of the DTLZ test function to be solved.
     *************************************************************/
    NSGA2_Solver(unsigned dtlz);

    /******************************
     * Constructs an empty solver.
     ******************************/
    NSGA2_Solver();

    /***********************
     * Solves the instance.
     ***********************/
    void solve();

    /***************************************************************
     * Standard stream operator.
     *
     * @param os the standard output stream object.
     * @param solver the solver.
     *
     * @return the stream object.
     ***************************************************************/
    friend std::ostream & operator <<(std::ostream & os,
                                      const NSGA2_Solver & solver);
};

}
