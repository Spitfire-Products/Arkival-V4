// C test functions for breadcrumb detection validation

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* basic_function() {
    return "test";
}

int function_with_params(const char* param1, int param2) {
    printf("%s_%d\n", param1, param2);
    return strlen(param1) + param2;
}

// Function without breadcrumb documentation
int undocumented_function() {
    return 1;
}

static void static_function(const char* data) {
    printf("Static: %s\n", data);
}

inline double inline_function(double value) {
    return value * 2.0;
}

void function_pointer_test(void (*callback)(int)) {
    callback(42);
}

void variadic_function(int count, ...) {
    printf("Variadic function with %d arguments\n", count);
}

struct TestStruct {
    int value;
    char name[50];
};

void struct_function(struct TestStruct* test_struct) {
    test_struct->value = 100;
    strcpy(test_struct->name, "modified");
}

void pointer_function(int* ptr, size_t size) {
    for (size_t i = 0; i < size; i++) {
        ptr[i] = i * 2;
    }
}

int array_function(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

void const_function(const char* const data) {
    printf("Const data: %s\n", data);
}

extern void extern_function(int value);

int recursive_function(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * recursive_function(n - 1);
}

int main(int argc, char* argv[]) {
    printf("C function tests ready\n");
    char* result = basic_function();
    printf("%s\n", result);
    return 0;
}