// TypeScript test functions for breadcrumb detection validation

interface TestInterface {
    id: number;
    name: string;
}

type TestType = {
    value: string;
    count: number;
};

function basicTypedFunction(param: string): string {
    return param.toUpperCase();
}

const complexTypedArrowFunction = (data: TestInterface, options?: TestType): Promise<string> => {
    return Promise.resolve(`${data.name}_${options?.value || 'default'}`);
};

// Function without breadcrumb documentation
function undocumentedTypedFunction(x: number, y: number): number {
    return x + y;
}

function genericFunction<T, U>(input: T, transform: (value: T) => U): U {
    return transform(input);
}

async function asyncGenericFunction<T extends string | number>(
    items: T[]
): Promise<T[]> {
    return items.filter(item => item !== null && item !== undefined);
}

function unionTypeFunction(
    param: string | number,
    config: { debug: boolean } & { verbose: boolean }
): string | number {
    return config.debug ? param.toString() : param;
}

class TestClass<T> {
    private data: T;
    
    constructor(data: T) {
        this.data = data;
    }
    
    public processData<U extends keyof T>(key: U): T[U] {
        return this.data[key];
    }
    
    // Method without breadcrumb
    public undocumentedMethod(): T {
        return this.data;
    }
    
    public static staticGenericMethod<T>(items: T[]): T | undefined {
        return items[0];
    }
}

function overloadedFunction(param: string): string;
function overloadedFunction(param: number): number;
function overloadedFunction(param: string | number): string | number {
    return typeof param === 'string' ? param.toUpperCase() : param * 2;
}

function isString(value: unknown): value is string {
    return typeof value === 'string';
}

const exportedTypedFunction = (
    callback: <T>(value: T) => T
): <U>(input: U) => U => {
    return callback;
};

// Decorator function
function LogMethod(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${propertyKey}`);
        return originalMethod.apply(this, args);
    };
}

// Namespace with functions
namespace TestNamespace {
    export function namespaceFunction(value: string): string {
        return value;
    }
    
    export const namespaceArrowFunction = (num: number): number => num * 2;
    
    // Undocumented namespace function
    export function undocumentedNamespaceFunction(): void {
        console.log("test");
    }
}

// Enum with computed values
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}

// Abstract class with abstract methods
abstract class AbstractTestClass {
    abstract abstractMethod(): void;
    
    protected concreteMethod(): string {
        return "concrete";
    }
    
    // Undocumented abstract method
    abstract undocumentedAbstractMethod(): number;
}

// Interface with optional and readonly properties
interface AdvancedInterface {
    readonly id: number;
    name?: string;
    process(data: unknown): void;
    optionalMethod?(): string;
}

// Mapped type functions
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

function makeReadonly<T>(obj: T): Readonly<T> {
    return Object.freeze({ ...obj });
}

// Conditional type function
type IsArray<T> = T extends any[] ? true : false;

function checkIfArray<T>(value: T): IsArray<T> {
    return Array.isArray(value) as IsArray<T>;
}

// Async generator function
async function* asyncGeneratorFunction(limit: number) {
    for (let i = 0; i < limit; i++) {
        yield await Promise.resolve(i);
    }
}

// Higher-order function with complex types
function createPipeline<T>(...fns: Array<(arg: T) => T>): (value: T) => T {
    return (value: T) => fns.reduce((v, fn) => fn(v), value);
}

// Method decorator example
class DecoratedClass {
    @LogMethod
    public decoratedMethod(input: string): string {
        return input.toUpperCase();
    }
    
    // Undocumented decorated method
    @LogMethod
    undocumentedDecoratedMethod(): void {
        // Do nothing
    }
}

// Module declaration
declare module "external-module" {
    export function externalFunction(param: string): void;
    export const externalConstant: number;
}

// Type guard with assertion
function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== 'string') {
        throw new Error('Value is not a string');
    }
}

// Readonly array function
function processReadonlyArray(items: readonly string[]): string {
    return items.join(', ');
}

// Tuple function
function processTuple(tuple: [string, number, boolean]): string {
    const [str, num, bool] = tuple;
    return `${str}: ${num} (${bool})`;
}

// Index signature function
interface StringDictionary {
    [key: string]: string;
}

function processStringDictionary(dict: StringDictionary): string[] {
    return Object.values(dict);
}

// Never type function
function throwError(message: string): never {
    throw new Error(message);
}

// Unknown type function
function processUnknown(value: unknown): string {
    if (typeof value === 'string') {
        return value;
    }
    return String(value);
}

// Intersection type function
type HasName = { name: string };
type HasAge = { age: number };

function processPersonData(person: HasName & HasAge): string {
    return `${person.name} is ${person.age} years old`;
}

// Literal type function
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

function makeRequest(method: HttpMethod, url: string): Promise<Response> {
    return fetch(url, { method });
}

// Recursive type function
type TreeNode<T> = {
    value: T;
    children?: TreeNode<T>[];
};

function traverseTree<T>(node: TreeNode<T>, callback: (value: T) => void): void {
    callback(node.value);
    node.children?.forEach(child => traverseTree(child, callback));
}