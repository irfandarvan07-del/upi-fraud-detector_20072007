#include "csv_reader.h"
#include <fstream>
#include <sstream>
#include <iostream>

std::vector<Txn> read_csv(const std::string &path) {
    std::vector<Txn> rows;
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "Failed to open CSV: " << path << std::endl;
        return rows;
    }
    std::string line;
    // read header
    if (!std::getline(file, line)) return rows;
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string token;
        Txn t;
        // txn_id
        std::getline(ss, token, ','); t.txn_id = token;
        // timestamp
        std::getline(ss, token, ','); t.timestamp = token;
        // from_vpa
        std::getline(ss, token, ','); t.from_vpa = token;
        // to_vpa
        std::getline(ss, token, ','); t.to_vpa = token;
        // amount
        std::getline(ss, token, ','); t.amount = token.empty() ? 0.0 : std::stod(token);
        // message
        std::getline(ss, token, ','); t.message = token;
        // is_new_payee
        std::getline(ss, token, ','); t.is_new_payee = token.empty() ? 0 : std::stoi(token);
        rows.push_back(t);
    }
    return rows;
}

