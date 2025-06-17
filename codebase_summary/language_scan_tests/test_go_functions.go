// Go test functions for breadcrumb detection validation
package main

import (
    "fmt"
    "context"
    "sync"
)

func basicFunction() string {
    return "test"
}

func functionWithParams(param1 string, param2 int) (string, error) {
    return fmt.Sprintf("%s_%d", param1, param2), nil
}

// Function without breadcrumb documentation
func undocumentedFunction() bool {
    return true
}

func variadicFunction(prefix string, items ...string) []string {
    result := make([]string, len(items))
    for i, item := range items {
        result[i] = prefix + item
    }
    return result
}

func genericFunction[T comparable](items []T) map[T]int {
    counts := make(map[T]int)
    for _, item := range items {
        counts[item]++
    }
    return counts
}

func contextFunction(ctx context.Context, data string) (string, error) {
    select {
    case <-ctx.Done():
        return "", ctx.Err()
    default:
        return data, nil
    }
}

type TestStruct struct {
    Value string
    Count int
}

func (t *TestStruct) Method(newValue string) {
    t.Value = newValue
}

// Method without breadcrumb
func (t TestStruct) UndocumentedMethod() string {
    return t.Value
}

func (t *TestStruct) PointerMethod() *string {
    return &t.Value
}

func (t TestStruct) ValueMethod() int {
    return t.Count
}

type TestInterface interface {
    InterfaceMethod(param string) error
}

func (t *TestStruct) InterfaceMethod(param string) error {
    t.Value = param
    return nil
}

func goroutineFunction(wg *sync.WaitGroup, ch chan<- string, data string) {
    defer wg.Done()
    ch <- data
}

func closureFunction(multiplier int) func(int) int {
    return func(x int) int {
        return x * multiplier
    }
}

func init() {
    fmt.Println("Go test package initialized")
}

func main() {
    fmt.Println("Go function tests ready")
    result := basicFunction()
    fmt.Println(result)
}