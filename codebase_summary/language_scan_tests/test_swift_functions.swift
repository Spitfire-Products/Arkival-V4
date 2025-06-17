// Swift test functions for breadcrumb detection validation

import Foundation

func basicFunction() -> String {
    return "test"
}

func functionWithParams(_ param1: String, param2: Int = 42) -> String {
    return "\(param1)_\(param2)"
}

// Function without breadcrumb documentation
func undocumentedFunction() -> Bool {
    return true
}

func genericFunction<T>(input: T) -> T {
    return input
}

func throwingFunction(input: String) throws -> String {
    guard !input.isEmpty else {
        throw NSError(domain: "TestError", code: 1, userInfo: nil)
    }
    return input.uppercased()
}

func asyncFunction(data: String) async -> String {
    return data.lowercased()
}

func asyncThrowingFunction(input: String) async throws -> String {
    guard !input.isEmpty else {
        throw NSError(domain: "AsyncError", code: 1, userInfo: nil)
    }
    return input
}

func closureFunction(completion: @escaping (String) -> Void) {
    completion("closure result")
}

func inoutFunction(value: inout String) {
    value = value.uppercased()
}

func variadicFunction(prefix: String, items: String...) -> [String] {
    return items.map { prefix + $0 }
}

struct TestStruct {
    var value: String
    
    init(value: String) {
        self.value = value
    }
    
    func getValue() -> String {
        return value
    }
    
    // Method without breadcrumb
    mutating func undocumentedMethod(newValue: String) {
        value = newValue
    }
    
    mutating func updateValue(_ newValue: String) {
        value = newValue
    }
    
    static func createDefault() -> TestStruct {
        return TestStruct(value: "default")
    }
}

class TestClass {
    var value: String
    
    init(value: String) {
        self.value = value
    }
    
    func classMethod() -> String {
        return value
    }
    
    class func classTypeMethod() -> String {
        return "class method"
    }
    
    final func finalMethod() -> String {
        return "final"
    }
    
    override func description() -> String {
        return value
    }
}

protocol TestProtocol {
    func protocolMethod() -> String
}

extension TestStruct: TestProtocol {
    func protocolMethod() -> String {
        return "protocol implementation"
    }
}

func +(left: TestStruct, right: TestStruct) -> TestStruct {
    return TestStruct(value: left.value + right.value)
}

extension TestClass {
    subscript(index: Int) -> Character? {
        guard index < value.count else { return nil }
        return value[value.index(value.startIndex, offsetBy: index)]
    }
}

func main() {
    print("Swift function tests ready")
    let result = basicFunction()
    print(result)
}

// Execute main function
main()