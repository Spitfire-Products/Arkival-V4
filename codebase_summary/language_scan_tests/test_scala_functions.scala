// Scala test functions for breadcrumb detection validation

// Basic function
def basicFunction(): String = {
  "test"
}

// Function with parameters
def functionWithParams(param1: String, param2: Int): String = {
  s"${param1}_${param2}"
}

// Function without breadcrumb documentation
def undocumentedFunction(): Boolean = {
  true
}

// Generic function
def genericFunction[T](value: T): T = {
  value
}

// Curried function
def curriedFunction(x: Int)(y: Int): Int = {
  x + y
}

// Class with methods
class TestClass(private var value: Int) {
  
  def getValue: Int = value
  
  // Method without breadcrumb
  def undocumentedMethod(): Unit = {
    value += 1
  }
  
  def updateValue(newValue: Int): Unit = {
    value = newValue
  }
}

// Object (singleton)
object TestObject {
  def objectMethod(param: String): String = {
    s"Object: $param"
  }
  
  // Undocumented object method
  def undocumentedObjectMethod(): String = {
    "undocumented"
  }
}

// Trait with methods
trait TestTrait {
  def traitMethod(value: Int): Int
  
  // Concrete method in trait
  def concreteTraitMethod(): String = {
    "trait method"
  }
}

// Case class
case class DataClass(name: String, value: Int) {
  def computeScore(): Double = {
    value * 1.5
  }
}

// Pattern matching function
def patternMatchFunction(input: Any): String = {
  input match {
    case s: String => s"String: $s"
    case i: Int => s"Int: $i"
    case _ => "Unknown"
  }
}

// Higher-order function
def higherOrderFunction(f: Int => Int): Int => Int = {
  x => f(x) * 2
}

// Partial function
val partialFunction: PartialFunction[Int, String] = {
  case 1 => "one"
  case 2 => "two"
  case _ => "other"
}

// Implicit function
implicit def stringToInt(s: String): Int = {
  s.length
}

// Lazy val function
lazy val lazyFunction: () => String = () => {
  "lazy evaluation"
}