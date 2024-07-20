#include "utils/argument_parser.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>

static inline
double multiplicative_epsilon_indicator(
        const std::vector<std::vector<double>> & reference_front,
        const std::vector<std::vector<double>> & front) {
    double epsilon = 0.0, min_max_ratio = 1.0, max_ratio, ratio;

    for(unsigned i = 0; i < reference_front.size(); i++) {
        for(unsigned j = 0; j < front.size(); j++) {
            max_ratio = 0.0;

            for(unsigned k = 0; k < reference_front[i].size() && k < front[j].size(); k++) {
                ratio = front[j][k] / reference_front[i][k];

                if(max_ratio < ratio) {
                    max_ratio = ratio;
                }
            }

            if(j == 0) {
                min_max_ratio = max_ratio;
            } else if (min_max_ratio > max_ratio) {
                min_max_ratio = max_ratio;
            }
        }

        if(i == 0) {
            epsilon = min_max_ratio;
        } else if(epsilon < min_max_ratio) {
            epsilon = min_max_ratio;
        }
    }

    return epsilon;
}

static inline
double inverse_multiplicative_epsilon_indicator(
        const std::vector<std::vector<double>> & reference_front,
        const std::vector<std::vector<double>> & front) {
    return 1.0 / multiplicative_epsilon_indicator(reference_front, front);
}

int main(int argc, char * argv[]) {
    Argument_Parser arg_parser(argc, argv);

    if(arg_parser.option_exists("--m") &&
       arg_parser.option_exists("--reference-pareto")) {
        std::ifstream ifs;
        unsigned m = std::stoul(arg_parser.option_value("--m")), num_solvers;
        std::vector<std::vector<double>> reference_pareto;
        std::vector<std::vector<std::vector<double>>> paretos;
        std::vector<std::vector<unsigned>> iteration_snapshots;
        std::vector<std::vector<double>> time_snapshots;
        std::vector<std::vector<std::vector<std::vector<double>>>>
            best_solutions_snapshots;

        ifs.open(arg_parser.option_value("--reference-pareto"));

        if(ifs.is_open()) {
            for(std::string line; std::getline(ifs, line);) {
                std::istringstream iss(line);
                std::vector<double> value(m, 0.0);

                for(unsigned j = 0; j < m; j++) {
                    iss >> value[j];
                }

                reference_pareto.push_back(value);
            }

            ifs.close();
        } else {
            throw std::runtime_error("File " +
                    arg_parser.option_value("--reference-pareto") +
                    " not found.");
        }

        for(num_solvers = 0;
            arg_parser.option_exists("--pareto-" +
                                     std::to_string(num_solvers)) ||
            arg_parser.option_exists("--best-solutions-snapshots-" +
                                     std::to_string(num_solvers)) ||
            arg_parser.option_exists("--multiplicative-epsilon-" +
                                     std::to_string(num_solvers)) ||
            arg_parser.option_exists("--multiplicative-epsilon-snapshots-" +
                                     std::to_string(num_solvers));
            num_solvers++) {}

        paretos.resize(num_solvers);
        iteration_snapshots.resize(num_solvers);
        time_snapshots.resize(num_solvers);
        best_solutions_snapshots.resize(num_solvers);

        for(unsigned i = 0; i < num_solvers; i++) {
            if(arg_parser.option_exists("--pareto-" + std::to_string(i))) {
                ifs.open(arg_parser.option_value("--pareto-" +
                                                 std::to_string(i)));

                if(ifs.is_open()) {
                    for(std::string line; std::getline(ifs, line);) {
                        std::istringstream iss(line);
                        std::vector<double> value(m, 0.0);

                        for(unsigned j = 0; j < m; j++) {
                            iss >> value[j];
                        }

                        paretos[i].push_back(value);
                    }

                    ifs.close();
                } else {
                    throw std::runtime_error("File " +
                            arg_parser.option_value("--pareto-" +
                                std::to_string(i)) + " not found.");
                }
            }
        }

        for(unsigned i = 0; i < num_solvers; i++) {
            if(arg_parser.option_exists("--best-solutions-snapshots-" +
                                        std::to_string(i))) {
                std::string best_solutions_snapshots_filename =
                    arg_parser.option_value("--best-solutions-snapshots-" +
                                            std::to_string(i));

                for(unsigned j = 0; ; j++) {
                    ifs.open(best_solutions_snapshots_filename +
                             std::to_string(j) + ".txt");

                    if(ifs.is_open()) {
                        unsigned iteration;
                        double time;

                        ifs >> iteration >> time;

                        iteration_snapshots[i].push_back(iteration);
                        time_snapshots[i].push_back(time);
                        best_solutions_snapshots[i].emplace_back();

                        ifs.ignore();

                        for(std::string line; std::getline(ifs, line);) {
                            std::istringstream iss(line);
                            std::vector<double> value(m, 0.0);

                            for(unsigned j = 0; j < m; j++) {
                                iss >> value[j];
                            }

                            best_solutions_snapshots[i].back().push_back(value);
                        }

                        ifs.close();
                    } else {
                        break;
                    }
                }
            }
        }

        for(unsigned i = 0; i < num_solvers; i++) {
            std::ofstream ofs;
            ofs.open(arg_parser.option_value("--multiplicative-epsilon-" +
                                             std::to_string(i)));

            if(ofs.is_open()) {
                double inverse_multiplicative_epsilon = inverse_multiplicative_epsilon_indicator(
                        reference_pareto,
                        paretos[i]);

                assert(inverse_multiplicative_epsilon >= 0.0);
                assert(inverse_multiplicative_epsilon <= 1.0);

                ofs << inverse_multiplicative_epsilon << std::endl;

                if(ofs.eof() || ofs.fail() || ofs.bad()) {
                    throw std::runtime_error("Error writing file " +
                            arg_parser.option_value("--multiplicative-epsilon-" +
                                std::to_string(i)) + ".");
                }

                ofs.close();
            } else {
                throw std::runtime_error("File " +
                        arg_parser.option_value("--multiplicative-epsilon-" +
                            std::to_string(i)) + " not created.");
            }
        }

        for(unsigned i = 0; i < num_solvers; i++) {
            std::ofstream ofs;

            ofs.open(arg_parser.option_value("--multiplicative-epsilon-snapshots-" +
                                             std::to_string(i)));

            if(ofs.is_open()) {
                for(unsigned j = 0;
                    j < best_solutions_snapshots[i].size();
                    j++) {
                    double inverse_multiplicative_epsilon = inverse_multiplicative_epsilon_indicator(
                            reference_pareto,
                            best_solutions_snapshots[i][j]);

                    assert(inverse_multiplicative_epsilon >= 0.0);
                    assert(inverse_multiplicative_epsilon <= 1.0);

                    ofs << iteration_snapshots[i][j] << ","
                        << time_snapshots[i][j] << ","
                        << inverse_multiplicative_epsilon << std::endl;

                    if(ofs.eof() || ofs.fail() || ofs.bad()) {
                        throw std::runtime_error("Error writing file " +
                                arg_parser.option_value(
                                    "--multiplicative-epsilon-snapshots-" +
                                    std::to_string(i)) + ".");
                    }
                }

                ofs.close();
            } else {
                throw std::runtime_error("File " +
                        arg_parser.option_value("--multiplicative-epsilon-snapshots-" +
                            std::to_string(i)) + " not created.");
            }
        }
    } else {
        std::cerr << "./multiplicative_epsilon_calculator_exec "
                  << "--m <m> "
                  << "--reference-pareto <reference_pareto_filename> "
                  << "--pareto-i <pareto_filename> "
                  << "--best-solutions-snapshots-i <best_solutions_snapshots_filename> "
                  << "--multiplicative-epsilon-i <multiplicative_epsilon_filename> "
                  << "--multiplicative-epsilon-snapshots-i <multiplicative_epsilon_snapshots_filename> "
                  << std::endl;
    }

    return 0;
}
