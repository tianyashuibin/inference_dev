#include <atomic>
#include <chrono>
#include <condition_variable>
#include <future>
#include <iostream>
#include <mutex>
#include <queue>
#include <shared_mutex>
#include <thread>
#include <vector>

using namespace std::chrono_literals;  // 让 100ms、2s 等字面量可用

// -------------------------------------------------------
// C++11/14/17/20 并发工具概览：
//   1. std::thread          — 创建和管理线程
//   2. std::mutex 系列      — 互斥锁（独占/共享/递归）
//   3. std::condition_variable — 条件变量，线程间通知
//   4. std::atomic          — 原子操作，无锁并发
//   5. std::future/promise  — 异步结果传递
//   6. std::async           — 高层异步任务
// -------------------------------------------------------


// ══════════════════════════════════════════════════════
// 1. std::thread — 基本线程
// ══════════════════════════════════════════════════════
void demo_thread() {
    std::cout << "\n=== 1. std::thread ===\n";

    // 创建线程：传函数 + 参数
    auto worker = [](int id, int ms) {
        std::this_thread::sleep_for(std::chrono::milliseconds(ms));
        std::cout << "  线程 " << id << " 完成（等待 " << ms << "ms）\n";
    };

    std::thread t1(worker, 1, 50);
    std::thread t2(worker, 2, 20);
    std::thread t3(worker, 3, 80);

    // join：等待线程结束；detach：让线程独立运行（不等待）
    t1.join();
    t2.join();
    t3.join();

    std::cout << "  所有线程已完成\n";
    std::cout << "  硬件并发数: " << std::thread::hardware_concurrency() << "\n";
}


// ══════════════════════════════════════════════════════
// 2. std::mutex — 互斥锁
// ══════════════════════════════════════════════════════
void demo_mutex() {
    std::cout << "\n=== 2. std::mutex / lock_guard / unique_lock ===\n";

    std::mutex mtx;
    int counter = 0;

    auto increment = [&](int n) {
        for (int i = 0; i < n; ++i) {
            // lock_guard：RAII 锁，构造时加锁，析构时解锁，不可手动释放
            std::lock_guard<std::mutex> lock(mtx);
            ++counter;
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i)
        threads.emplace_back(increment, 1000);
    for (auto& t : threads) t.join();

    std::cout << "  期望: 5000，实际: " << counter
              << (counter == 5000 ? "  ✓" : "  ✗ 数据竞争") << "\n";

    // unique_lock：更灵活，可手动 lock/unlock，可与条件变量配合
    std::mutex mtx2;
    {
        std::unique_lock<std::mutex> ul(mtx2);
        // ... 临界区 ...
        ul.unlock();   // 提前释放
        // ... 非临界区 ...
        ul.lock();     // 重新加锁
    }  // 析构时若仍持有锁则自动释放
    std::cout << "  unique_lock 演示完成\n";
}


// ══════════════════════════════════════════════════════
// 3. std::shared_mutex — 读写锁（C++17）
//    多个读者可同时持有共享锁；写者独占排他锁
// ══════════════════════════════════════════════════════
void demo_shared_mutex() {
    std::cout << "\n=== 3. shared_mutex（读写锁，C++17）===\n";

    std::shared_mutex rw_mtx;
    int data = 0;

    // 读线程：shared_lock 允许并发读
    auto reader = [&](int id) {
        std::shared_lock<std::shared_mutex> lock(rw_mtx);
        std::cout << "  读者 " << id << " 读到: " << data << "\n";
    };

    // 写线程：unique_lock 独占写
    auto writer = [&](int val) {
        std::unique_lock<std::shared_mutex> lock(rw_mtx);
        data = val;
        std::cout << "  写者 写入: " << val << "\n";
    };

    std::thread w1(writer, 42);
    w1.join();

    std::thread r1(reader, 1), r2(reader, 2), r3(reader, 3);
    r1.join(); r2.join(); r3.join();
}


// ══════════════════════════════════════════════════════
// 4. std::condition_variable — 条件变量
//    线程等待某个条件成立；另一线程修改条件后通知
// ══════════════════════════════════════════════════════

// 经典生产者-消费者模型
void demo_condition_variable() {
    std::cout << "\n=== 4. condition_variable（生产者-消费者）===\n";

    std::mutex mtx;
    std::condition_variable cv;
    std::queue<int> q;
    bool done = false;

    // 生产者
    std::thread producer([&] {
        for (int i = 1; i <= 5; ++i) {
            std::this_thread::sleep_for(30ms);
            {
                std::lock_guard<std::mutex> lock(mtx);
                q.push(i);
                std::cout << "  生产: " << i << "\n";
            }
            cv.notify_one();  // 通知一个等待线程
        }
        {
            std::lock_guard<std::mutex> lock(mtx);
            done = true;
        }
        cv.notify_all();  // 通知所有等待线程
    });

    // 消费者
    std::thread consumer([&] {
        while (true) {
            std::unique_lock<std::mutex> lock(mtx);
            // wait：释放锁并阻塞，直到 notify 且条件为 true 才继续
            // 第二个参数是谓词，防止虚假唤醒（spurious wakeup）
            cv.wait(lock, [&] { return !q.empty() || done; });

            while (!q.empty()) {
                std::cout << "  消费: " << q.front() << "\n";
                q.pop();
            }
            if (done) break;
        }
    });

    producer.join();
    consumer.join();
}


// ══════════════════════════════════════════════════════
// 5. std::atomic — 原子操作
//    对基本类型的读写保证原子性，无需加锁
// ══════════════════════════════════════════════════════
void demo_atomic() {
    std::cout << "\n=== 5. std::atomic ===\n";

    std::atomic<int> counter{0};

    auto increment = [&](int n) {
        for (int i = 0; i < n; ++i)
            counter.fetch_add(1, std::memory_order_relaxed);
            // 也可以写 ++counter 或 counter += 1
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i)
        threads.emplace_back(increment, 1000);
    for (auto& t : threads) t.join();

    std::cout << "  期望: 5000，实际: " << counter.load()
              << (counter == 5000 ? "  ✓" : "  ✗") << "\n";

    // compare_exchange：CAS 操作，无锁数据结构的基础
    std::atomic<int> val{10};
    int expected = 10;
    bool ok = val.compare_exchange_strong(expected, 20);
    // 若 val == expected(10)，则 val 设为 20，返回 true
    // 否则 expected 更新为 val 的当前值，返回 false
    std::cout << "  CAS(10→20): " << (ok ? "成功" : "失败")
              << "，val = " << val.load() << "\n";
}


// ══════════════════════════════════════════════════════
// 6. std::future / std::promise — 异步结果传递
//    promise 在一个线程写入结果，future 在另一个线程读取
// ══════════════════════════════════════════════════════
void demo_future_promise() {
    std::cout << "\n=== 6. future / promise ===\n";

    std::promise<int> prom;
    std::future<int> fut = prom.get_future();

    std::thread worker([&prom] {
        std::this_thread::sleep_for(50ms);
        prom.set_value(42);  // 写入结果
        std::cout << "  worker: 结果已设置\n";
    });

    std::cout << "  主线程: 等待结果...\n";
    int result = fut.get();  // 阻塞直到结果就绪
    std::cout << "  主线程: 收到结果 = " << result << "\n";

    worker.join();

    // packaged_task：把函数包装成 future
    std::packaged_task<int(int, int)> task([](int a, int b) { return a + b; });
    std::future<int> fut2 = task.get_future();
    std::thread t2(std::move(task), 10, 32);
    std::cout << "  packaged_task 结果: " << fut2.get() << "\n";
    t2.join();
}


// ══════════════════════════════════════════════════════
// 7. std::async — 高层异步任务
//    自动管理线程，直接返回 future
// ══════════════════════════════════════════════════════
void demo_async() {
    std::cout << "\n=== 7. std::async ===\n";

    // launch::async  — 立即在新线程执行
    // launch::deferred — 懒执行，调用 get()/wait() 时才在当前线程执行
    auto f1 = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(60ms);
        return 100;
    });

    auto f2 = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(40ms);
        return 200;
    });

    // 两个任务并行执行
    std::cout << "  f1 + f2 = " << f1.get() + f2.get() << "\n";

    // wait_for：非阻塞检查结果是否就绪
    auto f3 = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(200ms);
        return 999;
    });

    auto status = f3.wait_for(50ms);
    if (status == std::future_status::timeout)
        std::cout << "  f3 尚未就绪（超时）\n";
    std::cout << "  f3 最终结果: " << f3.get() << "\n";
}


// ══════════════════════════════════════════════════════
// 8. std::call_once — 保证只执行一次（单例初始化）
// ══════════════════════════════════════════════════════
void demo_call_once() {
    std::cout << "\n=== 8. call_once（线程安全的一次性初始化）===\n";

    std::once_flag flag;
    int init_count = 0;

    auto init = [&] {
        std::call_once(flag, [&] {
            ++init_count;
            std::cout << "  初始化执行了一次\n";
        });
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i)
        threads.emplace_back(init);
    for (auto& t : threads) t.join();

    std::cout << "  init_count = " << init_count << "（期望 1）\n";
}


int main() {
    demo_thread();
    demo_mutex();
    demo_shared_mutex();
    demo_condition_variable();
    demo_atomic();
    demo_future_promise();
    demo_async();
    demo_call_once();
    return 0;
}
