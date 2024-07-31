#include "utils/argument_parser.hpp"
#include <pagmo/utils/hypervolume.hpp>
#include <fstream>

static inline
double compute_hypervolume(
        const std::vector<double> & reference_point,
        const std::vector<std::vector<double>> & front) {
    std::vector<double> reference_point_prime(reference_point.size());
    std::vector<std::vector<double>> front_prime(front.size());

    for (unsigned i = 0; i < reference_point.size(); i++) {
        reference_point_prime[i] = reference_point[i];
    }

    for (unsigned i = 0; i < front.size(); i++) {
        front_prime[i] = std::vector<double>(front[i].size());
        for (unsigned j = 0; j < front[i].size(); j++) {
            front_prime[i][j] = front[i][j];
        }
    }

    pagmo::hypervolume hv(front_prime);
    return hv.compute(reference_point_prime);
}

static inline
double compute_hypervolume_ratio(
        const double & reference_hypervolume,
        const std::vector<double> & reference_point,
        const std::vector<std::vector<double>> & front) {
    double hypervolume = compute_hypervolume(reference_point, front);
    return hypervolume / reference_hypervolume;
}

int main(int argc, char * argv[]) {
    Argument_Parser arg_parser(argc, argv);

    if(arg_parser.option_exists("--m") &&
       arg_parser.option_exists("--reference-pareto")) {
        std::ifstream ifs;
        unsigned m = std::stoul(arg_parser.option_value("--m")), num_solvers;
        std::vector<double> reference_point(m, std::numeric_limits<double>::lowest());
        std::vector<std::vector<double>> reference_pareto;
        double reference_hypervolume;
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

                    if(reference_point[j] < value[j]) {
                        reference_point[j] = value[j];
                    }
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
            arg_parser.option_exists("--hypervolume-" +
                                     std::to_string(num_solvers)) ||
            arg_parser.option_exists("--hypervolume-snapshots-" +
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

                            if(reference_point[j] < value[j]) {
                                reference_point[j] = value[j];
                            }
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

                                if(reference_point[j] < value[j]) {
                                    reference_point[j] = value[j];
                                }
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

        reference_hypervolume = compute_hypervolume(reference_point,
                                                    reference_pareto);

        assert(reference_hypervolume > 0.0);

        for(unsigned i = 0; i < num_solvers; i++) {
            std::ofstream ofs;

            ofs.open(arg_parser.option_value("--hypervolume-" +
                                             std::to_string(i)));

            if(ofs.is_open()) {
                double hypervolume_ratio = compute_hypervolume_ratio(
                        reference_hypervolume,
                        reference_point,
                        paretos[i]);

                assert(hypervolume_ratio >= 0.0);
                // assert(hypervolume_ratio <= 1.0);

                ofs << hypervolume_ratio << std::endl;

                if(ofs.eof() || ofs.fail() || ofs.bad()) {
                    throw std::runtime_error("Error writing file " +
                            arg_parser.option_value("--hypervolume-" +
                                std::to_string(i)) + ".");
                }

                ofs.close();
            } else {
                throw std::runtime_error("File " +
                        arg_parser.option_value("--hypervolume-" +
                            std::to_string(i)) + " not created.");
            }
        }

        for(unsigned i = 0; i < num_solvers; i++) {
            std::ofstream ofs;

            ofs.open(arg_parser.option_value("--hypervolume-snapshots-" +
                                             std::to_string(i)));

            if(ofs.is_open()) {
                for(unsigned j = 0;
                    j < best_solutions_snapshots[i].size();
                    j++) {
                    double hypervolume_ratio = compute_hypervolume_ratio(
                            reference_hypervolume,
                            reference_point,
                            best_solutions_snapshots[i][j]);

                    assert(hypervolume_ratio >= 0.0);
                    // assert(hypervolume_ratio <= 1.0);

                    ofs << iteration_snapshots[i][j] << ","
                        << time_snapshots[i][j] << ","
                        << hypervolume_ratio << std::endl;

                    if(ofs.eof() || ofs.fail() || ofs.bad()) {
                        throw std::runtime_error("Error writing file " +
                                arg_parser.option_value(
                                    "--hypervolume-snapshots-" +
                                    std::to_string(i)) + ".");
                    }
                }

                ofs.close();
            } else {
                throw std::runtime_error("File " +
                        arg_parser.option_value("--hypervolume-snapshots-" +
                            std::to_string(i)) + " not created.");
            }
        }
    } else {
        std::cerr << "./hypervolume_calculator_exec "
                  << "--m <m> "
                  << "--reference-pareto <reference_pareto_filename> "
                  << "--pareto-i <pareto_filename> "
                  << "--best-solutions-snapshots-i <best_solutions_snapshots_filename> "
                  << "--hypervolume-i <hypervolume_filename> "
                  << "--hypervolume-snapshots-i <hypervolume_snapshots_filename> "
                  << std::endl;
    }

    return 0;
}
