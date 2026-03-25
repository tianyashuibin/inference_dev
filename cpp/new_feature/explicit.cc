#include <clocale>
#include <iostream>
#include <string>

// -------------------------------------------------------
// explicit 关键字：C++11 扩展
//
//   C++98: explicit 只能修饰单参数构造函数，禁止隐式转换
//   C++11: explicit 还可修饰转换运算符，禁止隐式类型转换
//   C++20: explicit(bool) — 条件性 explicit，用于模板元编程
// -------------------------------------------------------


// ── 1. 无 explicit：允许隐式转换 ──────────────────────────
struct Implicit {
    int value;
    Implicit(int v) : value(v) {}           // 可隐式转换
    operator std::string() const {          // 可隐式转换为 string
        return "Implicit(" + std::to_string(value) + ")";
    }
};

// ── 2. explicit 构造函数：禁止隐式转换 ────────────────────
struct Explicit {
    int value;
    explicit Explicit(int v) : value(v) {}  // 必须显式构造
    explicit operator std::string() const { // 必须显式转换
        return "Explicit(" + std::to_string(value) + ")";
    }
};

// ── 3. 多参数构造函数 + explicit（C++11）─────────────────
//    C++11 允许列表初始化触发多参数构造，explicit 同样可以阻止它
struct Point {
    int x, y;
    explicit Point(int x, int y) : x(x), y(y) {}
};

// ── 4. explicit(bool)：条件性 explicit（C++20）───────────
//    当模板参数支持无损转换时，允许隐式；否则要求显式
template <typename To, typename From>
struct Converter {
    From val;
    explicit(!std::is_convertible_v<From, To>) Converter(From v) : val(v) {}
};

// ── 辅助：接受 Implicit / Explicit 的函数，验证隐式转换 ──
void take_implicit(Implicit obj) {
    std::cout << "  take_implicit: value = " << obj.value << "\n";
}

// void take_explicit(Explicit obj) { ... }
// 若参数类型是 Explicit，调用 take_explicit(42) 会编译报错

int main() {
    std::setlocale(LC_ALL, "");

    // ── 1. 隐式构造：Implicit 允许，Explicit 不允许 ──────
    std::cout << "=== 隐式构造 ===\n";
    Implicit a = 42;          // OK：隐式 int → Implicit
    // Explicit b = 42;       // 错误：explicit 阻止隐式转换
    Explicit b(42);           // OK：显式构造
    Explicit c = Explicit(99);// OK：显式构造再拷贝/移动
    std::cout << "  a.value = " << a.value << "\n";
    std::cout << "  b.value = " << b.value << "\n";
    std::cout << "  c.value = " << c.value << "\n";

    // ── 2. 函数调用中的隐式转换 ────────────────────────
    std::cout << "\n=== 函数调用隐式转换 ===\n";
    take_implicit(7);         // OK：7 隐式转换为 Implicit(7)
    // take_explicit(7);      // 编译错误（已注释掉）
    std::cout << "  take_implicit(7) 成功\n";

    // ── 3. 隐式转换运算符 ──────────────────────────────
    std::cout << "\n=== 转换运算符 ===\n";
    std::string s1 = a;                    // OK：Implicit::operator string() 隐式触发
    // std::string s2 = b;                // 错误：explicit operator 不能隐式触发
    std::string s2 = static_cast<std::string>(b);  // OK：显式转换
    std::string s3 = (std::string)c;               // OK：C 风格显式转换
    std::cout << "  s1 = " << s1 << "\n";
    std::cout << "  s2 = " << s2 << "\n";
    std::cout << "  s3 = " << s3 << "\n";

    // ── 4. 条件表达式中的隐式 bool 转换 ─────────────────
    //    explicit operator bool() 在 if/while 中仍可隐式使用（特殊规则）
    std::cout << "\n=== explicit operator bool ===\n";
    struct Guard {
        bool ok;
        explicit operator bool() const { return ok; }
    };
    Guard g{true};
    if (g) std::cout << "  Guard 在 if 中隐式转 bool：OK\n";
    // bool flag = g;  // 错误：赋值场景不允许隐式转换
    bool flag = static_cast<bool>(g);
    std::cout << "  static_cast<bool>(g) = " << flag << "\n";

    // ── 5. 列表初始化与 explicit（C++11）─────────────────
    std::cout << "\n=== 列表初始化 ===\n";
    // Point p1 = {1, 2};  // 错误：explicit 阻止拷贝列表初始化
    Point p1{3, 4};         // OK：直接列表初始化
    Point p2(5, 6);         // OK：显式调用构造函数
    std::cout << "  p1 = (" << p1.x << ", " << p1.y << ")\n";
    std::cout << "  p2 = (" << p2.x << ", " << p2.y << ")\n";

    // ── 6. explicit(bool)：条件性 explicit（C++20）────────
    std::cout << "\n=== explicit(bool) / 条件性 explicit (C++20) ===\n";
    // int → double：is_convertible = true → 非 explicit，允许隐式构造
    Converter<double, int> ci = 10;            // OK：隐式
    std::cout << "  Converter<double,int>   隐式构造: " << ci.val << "\n";

    // int → std::string：is_convertible = false → explicit，必须显式构造
    // Converter<std::string, int> cs = 42;   // 错误：explicit 阻止隐式
    Converter<std::string, int> cs(42);        // OK：显式构造
    std::cout << "  Converter<string,int>  显式构造: " << cs.val << "\n";

    return 0;
}
