#include <iostream>
#include "csv_reader.h"
#include "detector.h"

int main(int argc, char** argv) {
    std::string path = "data/sample_txns.csv";
    if (argc > 1) path = argv[1];
    auto txns = read_csv(path);
    if (txns.empty()) {
        std::cerr << "No transactions read. Exiting.\n";
        return 1;
    }
    auto results = run_detection(txns);
    std::cout << "Detected results (severity>0):\n";
    std::cout << "txn_id,from_vpa,to_vpa,amount,severity,why\n";
    for (auto &r: results) {
        if (r.severity > 0) {
            std::cout << r.txn.txn_id << "," << r.txn.from_vpa << "," << r.txn.to_vpa
                      << "," << r.txn.amount << "," << r.severity << "," << r.why << "\n";
        }
    }
    return 0;
}

