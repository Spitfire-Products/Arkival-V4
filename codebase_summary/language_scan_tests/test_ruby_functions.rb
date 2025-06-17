# Ruby test functions for breadcrumb detection validation

def basic_method
  "test"
end

def method_with_params(param1, param2 = 42)
  "#{param1}_#{param2}"
end

# Method without breadcrumb documentation
def undocumented_method
  true
end

def block_method(&block)
  yield("test data") if block_given?
end

def splat_method(*args, **kwargs)
  { args: args, kwargs: kwargs }
end

def keyword_method(name:, age: 25, **options)
  { name: name, age: age, options: options }
end

class TestClass
  attr_accessor :value
  
  def initialize(value)
    @value = value
  end
  
  def instance_method
    @value.upcase
  end
  
  # Method without breadcrumb
  def undocumented_instance_method
    @value.downcase
  end
  
  def self.class_method(data)
    "Class: #{data}"
  end
  
  private
  
  def private_method
    "private"
  end
  
  protected
  
  def protected_method
    "protected"
  end
end

module TestModule
  def module_method
    "module method"
  end
  
  module_function
  
  def module_function_method
    "module function"
  end
end

obj = Object.new
def obj.singleton_method
  "singleton"
end

lambda_method = lambda { |x| x * 2 }

proc_method = Proc.new { |x| x.to_s }

alias_method :aliased_method, :basic_method

define_method(:dynamic_method) do |param|
  "Dynamic: #{param}"
end

CONSTANT_METHOD = -> { "constant lambda" }

def case_method(input)
  case input
  when String then input.upcase
  when Integer then input * 2
  else "unknown"
  end
end

def exception_method(input)
  raise ArgumentError, "Input cannot be nil" if input.nil?
  input.to_s
rescue StandardError => e
  "Error: #{e.message}"
end

def main
  puts "Ruby method tests ready"
  result = basic_method
  puts result
end

# Execute main method
main if __FILE__ == $0