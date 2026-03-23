#include <iostream>

// --- C++11: 递归展开，需要 base case ---
void printX() {}

template <typename T, typename... Args>
void printX(T first, Args... rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) std::cout << ", ";
    printX(rest...);
}

// --- C++17: fold expression，无需 base case ---
template <typename T, typename... Args>
void printX17(T&& first, Args&&... rest) {
    std::cout << first;
    ((std::cout << ", " << rest), ...);
}

int main() {
    std::cout << "C++11 recursive: ";
    printX(1, 3.14, "hello", 'A');
    std::cout << '\n';

    std::cout << "C++17 fold:      ";
    printX17(1, 3.14, "hello", 'A');
    std::cout << '\n';
}
