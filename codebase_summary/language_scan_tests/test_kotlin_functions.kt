// Kotlin test functions for breadcrumb detection validation

import kotlinx.coroutines.*

fun basicFunction(): String {
    return "test"
}

fun functionWithParams(param1: String, param2: Int = 42): String {
    return "${param1}_$param2"
}

// Function without breadcrumb documentation
fun undocumentedFunction(): Boolean {
    return true
}

suspend fun suspendFunction(data: String): String {
    delay(100)
    return data.uppercase()
}

inline fun inlineFunction(block: () -> Unit) {
    block()
}

fun <T> genericFunction(input: T): T {
    return input
}

fun String.extensionFunction(): String {
    return this.reversed()
}

class TestClass(private val value: String) {
    
    init {
        println("Initialized with: $value")
    }
    
    fun getValue(): String {
        return value
    }
    
    // Method without breadcrumb
    fun undocumentedMethod(): String {
        return value.lowercase()
    }
    
    companion object {
        fun createDefault(): TestClass {
            return TestClass("default")
        }
    }
}

data class DataClass(val name: String, val count: Int)

sealed class SealedClass {
    data class Success(val data: String) : SealedClass()
    data class Error(val message: String) : SealedClass()
}

interface TestInterface {
    fun interfaceMethod(): String
    
    fun defaultMethod(): String {
        return "default"
    }
}

object TestObject {
    fun objectMethod(): String {
        return "object method"
    }
}

fun higherOrderFunction(operation: (Int, Int) -> Int): (Int, Int) -> Int {
    return operation
}

val lambdaFunction = { x: Int, y: Int -> x + y }

val computedProperty: String
    get() = "computed"

fun main() {
    println("Kotlin function tests ready")
    val result = basicFunction()
    println(result)
}