# R test functions for breadcrumb detection validation

# Basic function
basic_function <- function() {
  return("test")
}

# Function with parameters
function_with_params <- function(param1, param2) {
  paste(param1, param2, sep = "_")
}

# Function without breadcrumb documentation
undocumented_function <- function() {
  TRUE
}

# Function with default parameters
default_params_function <- function(x = 10, y = 20) {
  x + y
}

# Function with variable arguments
variadic_function <- function(...) {
  args <- list(...)
  sum(unlist(args))
}

# Anonymous function assigned to variable
square_function <- function(x) x^2

# Function using formula syntax
model_function <- function(data) {
  lm(y ~ x, data = data)
}

# Generic function
calculate_mean <- function(x) {
  UseMethod("calculate_mean")
}

# Method for numeric
calculate_mean.numeric <- function(x) {
  mean(x, na.rm = TRUE)
}

# Method for data.frame
calculate_mean.data.frame <- function(x) {
  sapply(x, mean, na.rm = TRUE)
}

# Closure example
make_counter <- function() {
  count <- 0
  function() {
    count <<- count + 1
    count
  }
}

# Function with side effects
update_global <- function(value) {
  global_var <<- value
  invisible(NULL)
}

# Recursive function
factorial <- function(n) {
  if (n <= 1) {
    return(1)
  } else {
    return(n * factorial(n - 1))
  }
}

# Function returning function
create_multiplier <- function(factor) {
  function(x) x * factor
}

# Vectorized function
vectorized_operation <- function(x, y) {
  ifelse(x > y, x - y, y - x)
}

# Function with error handling
safe_divide <- function(x, y) {
  tryCatch({
    x / y
  }, error = function(e) {
    warning("Division error: ", e$message)
    NA
  })
}

# S3 class constructor
create_person <- function(name, age) {
  structure(
    list(name = name, age = age),
    class = "person"
  )
}

# Print method for person class
print.person <- function(x, ...) {
  cat("Person:", x$name, "Age:", x$age, "\n")
}

# Pipe-friendly function
process_data <- function(data, na.rm = TRUE) {
  data %>%
    na.omit() %>%
    scale() %>%
    as.data.frame()
}

# Undocumented utility function
utility_function <- function(vec) {
  vec[vec > mean(vec)]
}