#include "rules.h"
#include <algorithm>
#include <cctype>
#include <sstream>

static const std::vector<std::string> SUSP_WORDS = {
    "otp","pin","verify","verification","refund","urgent","send back"
};

bool contains_keyword(const std::string &s) {
    std::string lower;
    lower.reserve(s.size());
    for (char c: s) lower.push_back(std::tolower(c));
    for (auto &k: SUSP_WORDS) {
        if (lower.find(k) != std::string::npos) return true;
    }
    return false;
}

RuleResult apply_rules(const Txn &t) {
    RuleResult r;
    if (!t.message.empty() && contains_keyword(t.message)) {
        r.suspicious_msg = true;
        r.reasons.push_back("suspicious_message");
    }
    if (t.is_new_payee) {
        r.new_payee = true;
        r.reasons.push_back("new_payee");
    }
    if (t.amount > 5000.0) {
        r.high_amount = true;
        r.reasons.push_back("high_amount");
    }
    return r;
}

