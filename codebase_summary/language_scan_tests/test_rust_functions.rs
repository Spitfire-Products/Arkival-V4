// Rust test functions for breadcrumb detection validation

use std::collections::HashMap;
use std::fmt::Display;

fn basic_function() -> String {
    "test".to_string()
}

fn function_with_params(param1: &str, param2: i32) -> String {
    format!("{}_{}", param1, param2)
}

// Function without breadcrumb documentation
fn undocumented_function() -> bool {
    true
}

pub fn public_function(data: Vec<String>) -> usize {
    data.len()
}

async fn async_function(input: String) -> Result<String, Box<dyn std::error::Error>> {
    Ok(input.to_uppercase())
}

fn generic_function<T: Display + Clone>(input: T) -> String {
    format!("Value: {}", input)
}

struct TestStruct {
    value: String,
}

impl TestStruct {
    pub fn new(value: String) -> Self {
        Self { value }
    }
    
    pub fn get_value(&self) -> &str {
        &self.value
    }
    
    // Method without breadcrumb
    fn undocumented_method(&mut self, new_value: String) {
        self.value = new_value;
    }
    
    pub fn update_value(&mut self, new_value: String) -> &str {
        self.value = new_value;
        &self.value
    }
}

trait TestTrait {
    fn trait_method(&self) -> String;
}

impl TestTrait for TestStruct {
    fn trait_method(&self) -> String {
        format!("Trait: {}", self.value)
    }
}

pub fn error_handling_function(input: &str) -> Result<usize, &'static str> {
    if input.is_empty() {
        Err("Input cannot be empty")
    } else {
        Ok(input.len())
    }
}

const fn const_function(x: i32, y: i32) -> i32 {
    x + y
}

fn main() {
    println!("Rust function tests ready");
    let _ = basic_function();
    let _ = function_with_params("test", 42);
    let _ = public_function(vec!["a".to_string(), "b".to_string()]);
}