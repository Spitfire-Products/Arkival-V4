-- Lua test functions for breadcrumb detection validation

-- Basic function
function basicFunction()
    return "test"
end

-- Function with parameters
function functionWithParams(param1, param2)
    return param1 .. "_" .. tostring(param2)
end

-- Function without breadcrumb documentation
function undocumentedFunction()
    return true
end

-- Local function
local function localFunction(value)
    return value * 2
end

-- Function assigned to variable
myFunction = function(x, y)
    return x + y
end

-- Local function assigned to variable
local anotherFunction = function(text)
    print(text)
end

-- Table with methods
local MyTable = {}

function MyTable:new(value)
    local obj = {value = value}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function MyTable:getValue()
    return self.value
end

-- Function without breadcrumb
function MyTable:undocumentedMethod()
    self.value = self.value + 1
end

-- Closure example
function makeCounter()
    local count = 0
    return function()
        count = count + 1
        return count
    end
end

-- Variadic function
function variadicFunction(first, ...)
    local args = {...}
    return first, #args
end

-- Recursive function
function factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
    end
end

-- Coroutine function
function coroutineFunction()
    for i = 1, 10 do
        coroutine.yield(i)
    end
end

-- Module pattern
local M = {}

function M.moduleFunction(param)
    return "Module: " .. param
end

-- Undocumented module function
function M.undocumentedModuleFunction()
    return "undocumented"
end

return M