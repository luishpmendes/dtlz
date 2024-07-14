#pragma once

#include "chromosome.hpp"
#include <pagmo/problem.hpp>

namespace dtlz {

class Decoder {
    public:

    unsigned dtlz;

    unsigned n;

    unsigned m;

    pagmo::problem prob;

    Decoder(unsigned dtlz, unsigned n, unsigned m);

    std::vector<double> decode(NSBRKGA::Chromosome & chromosome, bool rewrite);
};

}
