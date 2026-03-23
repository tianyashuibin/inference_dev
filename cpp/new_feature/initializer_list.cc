#include <initializer_list>
#include <iostream>
#include <vector>
#include <string>

// 1. 函数接受 initializer_list 参数
void print_ints(std::initializer_list<int> list) {
    for (int val : list) {
        std::cout << val << " ";
    }
    std::cout << "\n";
}

// 2. 类中使用 initializer_list 构造函数
class NumberList {
public:
    std::vector<int> data;

    NumberList(std::initializer_list<int> init) : data(init) {
        std::cout << "Constructed with " << init.size() << " elements\n";
    }

    void print() const {
        for (int v : data) std::cout << v << " ";
        std::cout << "\n";
    }

    int sum() const {
        int s = 0;
        for (int v : data) s += v;
        return s;
    }
};

// 3. 模板函数 + initializer_list
template <typename T>
T max_of(std::initializer_list<T> list) {
    T result = *list.begin();
    for (const T& val : list) {
        if (val > result) result = val;
    }
    return result;
}

int main() {
    // 基本用法：直接传递花括号列表
    std::cout << "=== 函数参数 ===\n";
    print_ints({1, 2, 3, 4, 5});

    // 类构造函数中的 initializer_list
    std::cout << "\n=== 类构造 ===\n";
    NumberList nums = {10, 20, 30, 40};
    nums.print();
    std::cout << "Sum: " << nums.sum() << "\n";

    // 标准库容器同样支持 initializer_list 初始化
    std::cout << "\n=== 标准库容器 ===\n";
    std::vector<std::string> words = {"hello", "world", "cpp"};
    for (const auto& w : words) std::cout << w << " ";
    std::cout << "\n";

    // 模板函数
    std::cout << "\n=== 模板函数 ===\n";
    std::cout << "max_of ints:    " << max_of({3, 1, 4, 1, 5, 9, 2, 6}) << "\n";
    std::cout << "max_of doubles: " << max_of({1.1, 3.3, 2.2}) << "\n";

    // 赋值时使用 initializer_list
    std::cout << "\n=== 重新赋值 ===\n";
    nums = {100, 200, 300};
    nums.print();

    return 0;
}
