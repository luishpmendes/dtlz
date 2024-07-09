#include "solver/nsga2/nsga2_solver.hpp"

int main() {
    dtlz::NSGA2_Solver solver;

    for(unsigned dtlz = 1; dtlz <= 7; dtlz++) {
        solver = dtlz::NSGA2_Solver(dtlz);

        solver.set_seed(2351389233);
        solver.time_limit = 5.0;
        solver.iterations_limit = 100;
        solver.max_num_solutions = 64;
        solver.population_size = 32;
        solver.max_num_snapshots = 32;

        assert(solver.dtlz == dtlz);
        assert(solver.n == 5);
        assert(solver.m == 3);
        assert(solver.seed == 2351389233);
        assert(fabs(solver.time_limit - 5.0) <
                std::numeric_limits<double>::epsilon());
        assert(solver.iterations_limit == 100);
        assert(solver.max_num_solutions == 64);
        assert(solver.population_size == 32);
        assert(solver.max_num_snapshots == 32);
        assert(fabs(solver.crossover_probability - 0.95) <
                std::numeric_limits<double>::epsilon());
        assert(fabs(solver.crossover_distribution - 10.00) <
                std::numeric_limits<double>::epsilon());
        assert(fabs(solver.mutation_probability - 0.01) <
                std::numeric_limits<double>::epsilon());
        assert(fabs(solver.mutation_distribution - 50.00) <
                std::numeric_limits<double>::epsilon());

        solver.solve();

        assert(solver.solving_time > 0);

        assert(solver.num_iterations > 0);
        assert(solver.num_iterations <= solver.iterations_limit);

        assert(solver.best_individuals.size() > 0);
        assert(solver.best_individuals.size() <= solver.max_num_solutions);

        assert(solver.num_snapshots == solver.max_num_snapshots);

        assert(solver.best_solutions_snapshots.size() == solver.num_snapshots);
        assert(solver.num_non_dominated_snapshots.size() == solver.num_snapshots);
        assert(solver.num_fronts_snapshots.size() == solver.num_snapshots);
        assert(solver.populations_snapshots.size() == solver.num_snapshots);

        for(const auto & s1 : solver.best_individuals) {
            assert(s1.first.size() == solver.m);
            assert(s1.second.size() == solver.n);

            for(const auto & x : s1.second) {
                assert(x >= 0.0);
                assert(x <= 1.0);
            }

            for(const auto & s2 : solver.best_individuals) {
                bool dominates = dtlz::Solver::dominates(s1.first, s2.first),
                     is_dominated = dtlz::Solver::dominates(s2.first, s1.first);
                assert(!dominates);
                assert(!is_dominated);
            }
        }

        for(const auto & snapshot : solver.best_solutions_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for(const auto & s : std::get<2>(snapshot)) {
                assert(s.size() == solver.m);
            }
        }

        for(const auto & snapshot : solver.num_fronts_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for(const unsigned & num_fronts : std::get<2>(snapshot)) {
                assert(num_fronts > 0);
                assert(num_fronts <= solver.population_size);
            }
        }

        for(const auto & snapshot : solver.populations_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for(const auto & population : std::get<2>(snapshot)) {
                assert(population.size() == solver.population_size);

                for(const auto & s : population) {
                    assert(s.size() == solver.m);
                }
            }
        }

        std::cout << solver << std::endl;

        std::cout << "Num non dominated snapshots: ";
        for(unsigned i = 0;
            i < solver.num_non_dominated_snapshots.size() - 1;
            i++) {
            std::cout << std::get<2>(solver.num_non_dominated_snapshots[i]).front()
                    << " ";
        }
        std::cout << std::get<2>(solver.num_non_dominated_snapshots.back()).front()
                << std::endl;

        std::cout << "Num fronts snapshots: ";
        for(unsigned i = 0; i < solver.num_fronts_snapshots.size() - 1; i++) {
            std::cout << std::get<2>(solver.num_fronts_snapshots[i]).front()
                    << " ";
        }
        std::cout << std::get<2>(solver.num_fronts_snapshots.back()).front()
                << std::endl << std::endl;
    }

    return 0;
}
