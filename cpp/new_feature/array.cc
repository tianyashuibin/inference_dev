#include <array>
#include <algorithm>
#include <clocale>
#include <iostream>
#include <numeric>

// -------------------------------------------------------
// std::array 的核心特点：
//   1. 大小固定，编译期确定，是类型的一部分
//   2. 栈上分配，无堆内存开销
//   3. 不会退化为指针（区别于 C 原生数组）
//   4. 支持标准容器接口（迭代器、size()、at() 等）
// -------------------------------------------------------

// 接受 std::array 时大小是类型的一部分，不会退化为指针
void print(const std::array<int, 5>& arr) {
    for (int v : arr) std::cout << v << " ";
    std::cout << "\n";
}

// C 原生数组会退化为指针，丢失大小信息
void print_c_array(int* arr, size_t n) {   // 必须额外传 n
    for (size_t i = 0; i < n; ++i) std::cout << arr[i] << " ";
    std::cout << "\n";
}

int main() {
    std::setlocale(LC_ALL, "");
    // 1. 初始化
    std::cout << "=== 初始化 ===\n";
    std::array<int, 5> a = {3, 1, 4, 1, 5};
    std::array<int, 5> b{};           // 零初始化
    std::array<int, 3> c = {7, 8, 9};

    print(a);
    print(b);  // 全 0

    // 2. 大小是类型的一部分（编译期）
    std::cout << "\n=== 大小是类型的一部分 ===\n";
    std::cout << "a.size() = " << a.size() << "\n";
    // std::array<int,5> 和 std::array<int,3> 是不同类型
    // print(c);  // 编译错误！大小不匹配

    // 3. 随机访问：[] 不检查越界，at() 检查
    std::cout << "\n=== 元素访问 ===\n";
    std::cout << "a[2]    = " << a[2] << "\n";
    std::cout << "a.at(2) = " << a.at(2) << "\n";
    std::cout << "front   = " << a.front() << ", back = " << a.back() << "\n";

    // 4. 栈分配 vs vector 堆分配
    std::cout << "\n=== 栈上分配 ===\n";
    std::cout << "data() 指针（栈地址）: " << a.data() << "\n";

    // 5. 支持标准算法
    std::cout << "\n=== 标准算法 ===\n";
    std::array<int, 5> sorted = a;
    std::sort(sorted.begin(), sorted.end());
    print(sorted);

    int total = std::accumulate(a.begin(), a.end(), 0);
    std::cout << "sum = " << total << "\n";

    auto it = std::find(a.begin(), a.end(), 4);
    std::cout << "find(4): index = " << (it - a.begin()) << "\n";

    // 6. 不退化为指针（与 C 数组对比）
    std::cout << "\n=== 不退化为指针 ===\n";
    int raw[5] = {1, 2, 3, 4, 5};
    // sizeof(raw) / sizeof(raw[0]) 在函数内有效，传参后丢失
    print_c_array(raw, 5);          // 必须手动传大小
    // std::array 始终携带大小
    std::cout << "std::array 始终知道自己的大小: " << a.size() << "\n";

    // 7. 支持拷贝赋值（C 数组不支持）
    std::cout << "\n=== 拷贝赋值 ===\n";
    std::array<int, 5> copy = a;    // 直接拷贝，C 数组做不到
    copy[0] = 99;
    std::cout << "original: "; print(a);
    std::cout << "copy:     "; print(copy);

    // 8. 结构化绑定（C++17）
    std::cout << "\n=== 结构化绑定 (C++17) ===\n";
    std::array<int, 3> rgb = {255, 128, 0};
    auto [r, g, b2] = rgb;
    std::cout << "r=" << r << " g=" << g << " b=" << b2 << "\n";

    return 0;
}
