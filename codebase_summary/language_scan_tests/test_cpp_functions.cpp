// C++ test functions for breadcrumb detection validation

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <functional>

std::string basicFunction() {
    return "test";
}

std::string functionWithParams(const std::string& param1, int param2) {
    return param1 + "_" + std::to_string(param2);
}

// Function without breadcrumb documentation
bool undocumentedFunction() {
    return true;
}

template<typename T>
T templateFunction(const T& input) {
    return input;
}

constexpr int constexprFunction(int x, int y) {
    return x + y;
}

inline double inlineFunction(double value) {
    return value * 2.0;
}

class TestClass {
public:
    TestClass(const std::string& value) : value_(value) {}
    
    ~TestClass() = default;
    
    std::string getValue() const {
        return value_;
    }
    
    // Method without breadcrumb
    void undocumentedMethod(const std::string& newValue) {
        value_ = newValue;
    }
    
    static TestClass createDefault() {
        return TestClass("default");
    }
    
    virtual void virtualMethod() {
        std::cout << "Virtual method called" << std::endl;
    }
    
    virtual void pureVirtualMethod() = 0;

private:
    std::string value_;
};

class FriendTestClass {
    friend void friendFunction(FriendTestClass& obj);
private:
    int privateValue = 42;
};

void friendFunction(FriendTestClass& obj) {
    obj.privateValue = 100;
}

namespace TestNamespace {
    void namespaceFunction(const std::string& data) {
        std::cout << "Namespace: " << data << std::endl;
    }
}

auto lambdaFunction = [](int x, int y) -> int {
    return x * y;
};

void functionPointerTest(std::function<void(int)> callback) {
    callback(42);
}

class OperatorTestClass {
public:
    bool operator==(const OperatorTestClass& other) const {
        return true;
    }
};

int main() {
    std::cout << "C++ function tests ready" << std::endl;
    std::string result = basicFunction();
    std::cout << result << std::endl;
    return 0;
}