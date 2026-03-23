#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {5, 2, 8, 1, 9, 3};

    // 基本 lambda
    auto square = [](int x) { return x * x; };
    std::cout << "square(4) = " << square(4) << '\n';

    // 捕获外部变量（by value）
    int threshold = 5;
    auto above = [threshold](int x) { return x > threshold; };

    // 配合标准库算法
    std::cout << "sort:    ";
    std::sort(nums.begin(), nums.end());
    for (int n : nums) std::cout << n << ' ';
    std::cout << '\n';

    std::cout << "above 5: ";
    for (int n : nums)
        if (above(n)) std::cout << n << ' ';
    std::cout << '\n';

    // 捕获（by reference），修改外部变量
    int sum = 0;
    std::for_each(nums.begin(), nums.end(), [&sum](int x) { sum += x; });
    std::cout << "sum =    " << sum << '\n';

    // 泛型 lambda（C++14）
    auto add = [](auto a, auto b) { return a + b; };
    std::cout << "add(1, 2)       = " << add(1, 2) << '\n';
    std::cout << "add(1.5, 2.5)   = " << add(1.5, 2.5) << '\n';
}
