// C# test functions for breadcrumb detection validation

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace TestNamespace
{
    // Basic class with methods
    public class TestClass
    {
        private int value;

        // Constructor
        public TestClass(int initialValue)
        {
            value = initialValue;
        }

        // Basic method
        public string BasicMethod()
        {
            return "test";
        }

        // Method with parameters
        public string MethodWithParams(string param1, int param2)
        {
            return $"{param1}_{param2}";
        }

        // Method without breadcrumb documentation
        public bool UndocumentedMethod()
        {
            return true;
        }

        // Property with getter and setter
        public int Value
        {
            get { return value; }
            set { this.value = value; }
        }

        // Auto-implemented property
        public string Name { get; set; }

        // Static method
        public static TestClass CreateDefault()
        {
            return new TestClass(0);
        }

        // Async method
        public async Task<string> AsyncMethod()
        {
            await Task.Delay(100);
            return "async result";
        }

        // Generic method
        public T GenericMethod<T>(T input)
        {
            return input;
        }

        // Method with optional parameters
        public int OptionalParamsMethod(int required, int optional = 10)
        {
            return required + optional;
        }

        // Method with out parameter
        public bool TryParse(string input, out int result)
        {
            return int.TryParse(input, out result);
        }

        // Method with ref parameter
        public void ModifyValue(ref int number)
        {
            number *= 2;
        }

        // Method with params array
        public int SumNumbers(params int[] numbers)
        {
            return numbers.Sum();
        }

        // Virtual method
        public virtual string VirtualMethod()
        {
            return "base";
        }

        // Protected method
        protected void ProtectedMethod()
        {
            Console.WriteLine("Protected");
        }

        // Private method
        private void PrivateMethod()
        {
            value++;
        }

        // Method returning tuple
        public (string name, int value) GetTuple()
        {
            return ("test", 42);
        }

        // Expression-bodied method
        public int DoubleValue() => value * 2;

        // Destructor/Finalizer
        ~TestClass()
        {
            // Cleanup
        }
    }

    // Interface definition
    public interface ITestInterface
    {
        void InterfaceMethod();
        string InterfaceProperty { get; set; }
        
        // Default interface method (C# 8+)
        public void DefaultMethod()
        {
            Console.WriteLine("Default implementation");
        }
    }

    // Abstract class
    public abstract class AbstractClass
    {
        public abstract void AbstractMethod();

        // Virtual method
        public virtual string VirtualMethod()
        {
            return "base implementation";
        }

        // Concrete method
        public void ConcreteMethod()
        {
            Console.WriteLine("Concrete");
        }
    }

    // Derived class
    public class DerivedClass : AbstractClass
    {
        public override void AbstractMethod()
        {
            Console.WriteLine("Implemented");
        }

        public override string VirtualMethod()
        {
            return "overridden";
        }

        // New method hiding base
        public new void ConcreteMethod()
        {
            Console.WriteLine("Hidden");
        }
    }

    // Partial class
    public partial class PartialClass
    {
        public void PartialMethod1()
        {
            Console.WriteLine("Part 1");
        }

        partial void OnSomethingHappened();
    }

    public partial class PartialClass
    {
        public void PartialMethod2()
        {
            Console.WriteLine("Part 2");
        }

        partial void OnSomethingHappened()
        {
            Console.WriteLine("Partial method implementation");
        }
    }

    // Static class with extension methods
    public static class ExtensionMethods
    {
        public static bool IsNullOrEmpty(this string str)
        {
            return string.IsNullOrEmpty(str);
        }

        // Undocumented extension method
        public static T FirstOrDefault<T>(this IEnumerable<T> source)
        {
            return source.FirstOrDefault();
        }

        public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T> source) where T : class
        {
            return source.Where(x => x != null);
        }
    }

    // Delegate and event
    public delegate void EventHandler(object sender, EventArgs e);

    public class EventClass
    {
        public event EventHandler SomethingHappened;

        protected virtual void OnSomethingHappened()
        {
            SomethingHappened?.Invoke(this, EventArgs.Empty);
        }

        public void TriggerEvent()
        {
            OnSomethingHappened();
        }
    }

    // Generic class with constraints
    public class GenericClass<T> where T : class, new()
    {
        private T data;

        public GenericClass()
        {
            data = new T();
        }

        public T GetData()
        {
            return data;
        }

        public void SetData(T value)
        {
            data = value;
        }

        // Generic method with different type
        public U ConvertTo<U>(Func<T, U> converter)
        {
            return converter(data);
        }
    }

    // Struct definition
    public struct Point
    {
        public int X { get; set; }
        public int Y { get; set; }

        public Point(int x, int y)
        {
            X = x;
            Y = y;
        }

        public double DistanceFromOrigin()
        {
            return Math.Sqrt(X * X + Y * Y);
        }

        // Readonly method (C# 8+)
        public readonly override string ToString()
        {
            return $"({X}, {Y})";
        }
    }

    // Enum with custom values
    public enum Status
    {
        Active = 1,
        Inactive = 2,
        Pending = 3
    }

    // Lambda expressions and LINQ
    public class LinqExamples
    {
        private List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

        public IEnumerable<int> FilterEven()
        {
            return numbers.Where(n => n % 2 == 0);
        }

        // Expression-bodied member
        public int Sum() => numbers.Sum();

        // Local function
        public int Calculate(int x)
        {
            return LocalFunction(x);

            int LocalFunction(int value)
            {
                return value * 2;
            }
        }

        // Method with yield return
        public IEnumerable<int> GetSquares()
        {
            foreach (var num in numbers)
            {
                yield return num * num;
            }
        }

        // Async enumerable (C# 8+)
        public async IAsyncEnumerable<int> GetAsyncNumbers()
        {
            foreach (var num in numbers)
            {
                await Task.Delay(100);
                yield return num;
            }
        }
    }

    // Record type (C# 9+)
    public record Person(string FirstName, string LastName)
    {
        public string FullName => $"{FirstName} {LastName}";

        public void PrintName()
        {
            Console.WriteLine(FullName);
        }
    }

    // Nested class
    public class OuterClass
    {
        public void OuterMethod()
        {
            var inner = new InnerClass();
            inner.InnerMethod();
        }

        private class InnerClass
        {
            public void InnerMethod()
            {
                Console.WriteLine("Inner");
            }
        }
    }

    // Indexer example
    public class IndexerClass
    {
        private string[] data = new string[10];

        public string this[int index]
        {
            get { return data[index]; }
            set { data[index] = value; }
        }

        // Named indexer
        public string this[string key]
        {
            get { return data[0]; }
            set { data[0] = value; }
        }
    }

    // Operator overloading
    public class Vector
    {
        public double X { get; set; }
        public double Y { get; set; }

        public static Vector operator +(Vector v1, Vector v2)
        {
            return new Vector { X = v1.X + v2.X, Y = v1.Y + v2.Y };
        }

        public static bool operator ==(Vector v1, Vector v2)
        {
            return v1.X == v2.X && v1.Y == v2.Y;
        }

        public static bool operator !=(Vector v1, Vector v2)
        {
            return !(v1 == v2);
        }

        public override bool Equals(object obj)
        {
            if (obj is Vector other)
                return this == other;
            return false;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(X, Y);
        }
    }

    // Pattern matching examples
    public class PatternMatching
    {
        public string CheckType(object obj)
        {
            return obj switch
            {
                int i => $"Integer: {i}",
                string s => $"String: {s}",
                null => "Null",
                _ => "Unknown"
            };
        }

        public void PropertyPattern(Person person)
        {
            if (person is { FirstName: "John", LastName: "Doe" })
            {
                Console.WriteLine("Found John Doe");
            }
        }

        // Tuple pattern
        public string ClassifyPoint((int x, int y) point) => point switch
        {
            (0, 0) => "Origin",
            (_, 0) => "On X-axis",
            (0, _) => "On Y-axis",
            _ => "Other"
        };
    }

    // Undocumented utility class
    public static class UtilityClass
    {
        public static void UtilityMethod()
        {
            Console.WriteLine("Utility");
        }

        public static T Max<T>(T a, T b) where T : IComparable<T>
        {
            return a.CompareTo(b) > 0 ? a : b;
        }

        public static async Task<string> AsyncUtility()
        {
            await Task.Delay(100);
            return "Done";
        }
    }

    // Nullable reference types (C# 8+)
    public class NullableExample
    {
        public string? NullableMethod(string? input)
        {
            return input?.ToUpper();
        }

        public void HandleNullable(string? text)
        {
            if (text is not null)
            {
                Console.WriteLine(text.Length);
            }
        }
    }

    // Init-only properties (C# 9+)
    public class InitOnlyClass
    {
        public string Name { get; init; }
        public int Value { get; init; }

        public void ProcessData()
        {
            Console.WriteLine($"{Name}: {Value}");
        }
    }
}