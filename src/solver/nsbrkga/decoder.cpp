#include "decoder.hpp"
#include <pagmo/problems/dtlz.hpp>
#include <cmath>

namespace dtlz {

Decoder::Decoder(unsigned dtlz, unsigned n, unsigned m) : dtlz(dtlz), n(n), m(m) {
    this->prob = pagmo::dtlz(this->dtlz, this->n, this->m);
}

std::vector<double> Decoder::decode(NSBRKGA::Chromosome & chromosome, 
                                    bool /* not used */) {
    pagmo::vector_double dv(chromosome);

    return this->prob.fitness(dv);
}

}
