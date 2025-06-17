<?php
// PHP test functions for breadcrumb detection validation

function basicFunction(): string {
    return "test";
}

function functionWithParams(string $param1, int $param2 = 42): string {
    return $param1 . "_" . $param2;
}

// Function without breadcrumb documentation
function undocumentedFunction(): bool {
    return true;
}

function nullableFunction(?string $param): ?string {
    return $param ? strtoupper($param) : null;
}

function variadicFunction(string $prefix, string ...$items): array {
    return array_map(fn($item) => $prefix . $item, $items);
}

$anonymousFunction = function(array $data): int {
    return count($data);
};

$arrowFunction = fn(int $x, int $y): int => $x + $y;

class TestClass {
    private string $value;
    
    public function __construct(string $value) {
        $this->value = $value;
    }
    
    public function getValue(): string {
        return $this->value;
    }
    
    // Method without breadcrumb
    public function undocumentedMethod(string $newValue): void {
        $this->value = $newValue;
    }
    
    public static function createDefault(): self {
        return new self("default");
    }
    
    public function __toString(): string {
        return $this->value;
    }
    
    abstract class AbstractClass {
        abstract public function abstractMethod(): void;
    }
}

interface TestInterface {
    public function interfaceMethod(string $param): bool;
}

trait TestTrait {
    public function traitMethod(): string {
        return "trait method";
    }
}

namespace TestNamespace {
    function namespaceFunction(string $data): void {
        echo "Namespace: " . $data . "\n";
    }
}

function generatorFunction(array $items): \Generator {
    foreach ($items as $item) {
        yield strtoupper($item);
    }
}

/**
 * @template T
 * @param T $input
 * @return T
 */
function genericFunction($input) {
    return $input;
}

function errorHandlingFunction(string $input): string {
    if (empty($input)) {
        throw new InvalidArgumentException("Input cannot be empty");
    }
    return $input;
}

function main(): void {
    echo "PHP function tests ready\n";
    $result = basicFunction();
    echo $result . "\n";
}

// Execute main function
main();
?>