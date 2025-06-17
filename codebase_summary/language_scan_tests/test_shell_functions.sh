#!/bin/bash
# Shell/Bash test functions for breadcrumb detection validation

# Basic function
function basic_function() {
    echo "test"
}

# Function with parameters
function function_with_params() {
    local param1=$1
    local param2=$2
    echo "${param1}_${param2}"
}

# Function without breadcrumb documentation
undocumented_function() {
    return 0
}

# Alternative function syntax
another_function() {
    echo "alternative syntax"
}

# Function with local variables
local_vars_function() {
    local var1="local"
    local var2="variables"
    echo "$var1 $var2"
}

# Function with return value
calculate_sum() {
    local a=$1
    local b=$2
    return $((a + b))
}

# Function using global variable
global_var="initial"
modify_global() {
    global_var="modified"
}

# Function with conditional logic
check_file() {
    if [ -f "$1" ]; then
        echo "File exists"
        return 0
    else
        echo "File not found"
        return 1
    fi
}

# Function with loop
process_array() {
    local arr=("$@")
    for item in "${arr[@]}"; do
        echo "Processing: $item"
    done
}

# Function with case statement
handle_option() {
    case "$1" in
        start)
            echo "Starting..."
            ;;
        stop)
            echo "Stopping..."
            ;;
        *)
            echo "Unknown option"
            ;;
    esac
}

# Recursive function
factorial() {
    local n=$1
    if [ $n -le 1 ]; then
        echo 1
    else
        echo $((n * $(factorial $((n - 1)))))
    fi
}

# Function with error handling
safe_divide() {
    if [ $2 -eq 0 ]; then
        echo "Error: Division by zero"
        return 1
    fi
    echo $(($1 / $2))
}

# Function using command substitution
get_system_info() {
    local hostname=$(hostname)
    local kernel=$(uname -r)
    echo "Host: $hostname, Kernel: $kernel"
}

# Function with here document
create_config() {
    cat << EOF > config.tmp
# Configuration file
host=$1
port=$2
EOF
}

# Undocumented utility function
utility_function() {
    find . -name "*.log" -mtime +7 -delete
}

# Function with getopts
parse_options() {
    while getopts "hv:f:" opt; do
        case $opt in
            h)
                echo "Help message"
                ;;
            v)
                echo "Version: $OPTARG"
                ;;
            f)
                echo "File: $OPTARG"
                ;;
            \?)
                echo "Invalid option"
                ;;
        esac
    done
}

# One-liner function
oneliner() { echo "One line function"; }

# Function with trap
cleanup_function() {
    trap 'echo "Cleaning up..."; rm -f /tmp/tempfile' EXIT
    # Do work here
}

# Function with array manipulation
array_operations() {
    local -a my_array=(one two three)
    my_array+=("four")
    echo "${my_array[@]}"
    echo "Array length: ${#my_array[@]}"
}