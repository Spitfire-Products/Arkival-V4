// Dart test functions for breadcrumb detection validation

import 'dart:async';
import 'dart:math';

String basicFunction() {
  return "test";
}

String functionWithParams(String param1, [int param2 = 42]) {
  return '${param1}_$param2';
}

// Function without breadcrumb documentation
bool undocumentedFunction() {
  return true;
}

Future<String> asyncFunction(String data) async {
  await Future.delayed(Duration(milliseconds: 100));
  return data.toUpperCase();
}

T genericFunction<T>(T input) {
  return input;
}

String namedParameterFunction({required String name, int age = 25}) {
  return '$name is $age years old';
}

int optionalParameterFunction(int x, [int? y, int z = 10]) {
  return x + (y ?? 0) + z;
}

class TestClass {
  String _value;
  
  TestClass(this._value);
  
  TestClass.fromString(String value) : _value = value;
  
  String get value => _value;
  
  set value(String newValue) => _value = newValue;
  
  String getValue() {
    return _value;
  }
  
  // Method without breadcrumb
  void undocumentedMethod() {
    _value = _value.toLowerCase();
  }
  
  static TestClass createDefault() {
    return TestClass("default");
  }
}

abstract class AbstractClass {
  void abstractMethod();
  
  void concreteMethod() {
    print("concrete");
  }
}

mixin TestMixin {
  void mixinMethod() {
    print("mixin method");
  }
}

extension StringExtension on String {
  String reverse() {
    return split('').reversed.join('');
  }
}

typedef StringProcessor = String Function(String);

String processString(String input, StringProcessor processor) {
  return processor(input);
}

Iterable<int> generatorFunction(int start, int end) sync* {
  for (int i = start; i <= end; i++) {
    yield i;
  }
}

Stream<String> streamFunction(List<String> items) async* {
  for (String item in items) {
    await Future.delayed(Duration(milliseconds: 50));
    yield item.toUpperCase();
  }
}

void main() {
  print("Dart function tests ready");
  String result = basicFunction();
  print(result);
}