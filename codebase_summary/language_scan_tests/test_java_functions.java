// Java test functions for breadcrumb detection validation

import java.util.*;
import java.util.concurrent.CompletableFuture;

public class TestJavaFunctions {
    
    public static String basicMethod() {
        return "test";
    }
    
    public String methodWithParams(String param1, int param2) {
        return param1 + "_" + param2;
    }
    
    // Method without breadcrumb documentation
    public boolean undocumentedMethod() {
        return true;
    }
    
    public <T> List<T> genericMethod(T... items) {
        return Arrays.asList(items);
    }
    
    public static void staticMethod(String data) {
        System.out.println(data);
    }
    
    public synchronized String synchronizedMethod(String input) {
        return input.toUpperCase();
    }
    
    public abstract class AbstractClass {
        public abstract void abstractMethod();
    }
    
    public interface TestInterface {
        void interfaceMethod(String param);
        
        default String defaultMethod() {
            return "default";
        }
    }
    
    public void lambdaMethod() {
        Runnable lambda = () -> System.out.println("Lambda executed");
        lambda.run();
    }
    
    public List<String> streamMethod(List<String> input) {
        return input.stream()
                   .filter(s -> s.length() > 3)
                   .map(String::toUpperCase)
                   .collect(Collectors.toList());
    }
    
    public CompletableFuture<String> asyncMethod(String data) {
        return CompletableFuture.supplyAsync(() -> data.toLowerCase());
    }
    
    public TestJavaFunctions(String initialValue) {
        this.value = initialValue;
    }
    
    private String value;
    
    public String getValue() {
        return value;
    }
    
    public void setValue(String newValue) {
        this.value = newValue;
    }
    
    public static void main(String[] args) {
        System.out.println("Java function tests ready");
        String result = basicMethod();
        System.out.println(result);
    }
}