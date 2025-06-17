// Objective-C test functions for breadcrumb detection validation

#import <Foundation/Foundation.h>

// Basic function
NSString *basicFunction() {
    return @"test";
}

// Function with parameters
NSString *functionWithParams(NSString *param1, int param2) {
    return [NSString stringWithFormat:@"%@_%d", param1, param2];
}

// Static function without breadcrumb
static BOOL undocumentedFunction() {
    return YES;
}

// Interface declaration
@interface TestClass : NSObject {
    NSInteger value;
}

@property (nonatomic, assign) NSInteger value;

- (instancetype)initWithValue:(NSInteger)val;
- (NSInteger)getValue;
- (void)undocumentedMethod;
- (void)updateValue:(NSInteger)newValue;
+ (instancetype)createDefault;

@end

// Implementation
@implementation TestClass

@synthesize value;

// Initializer
- (instancetype)initWithValue:(NSInteger)val {
    self = [super init];
    if (self) {
        value = val;
    }
    return self;
}

// Getter method
- (NSInteger)getValue {
    return value;
}

// Method without breadcrumb
- (void)undocumentedMethod {
    value++;
}

// Setter-like method
- (void)updateValue:(NSInteger)newValue {
    value = newValue;
}

// Class method
+ (instancetype)createDefault {
    return [[TestClass alloc] initWithValue:0];
}

@end

// Category extension
@interface TestClass (Extensions)
- (NSString *)description;
- (BOOL)isValid;
@end

@implementation TestClass (Extensions)

// Description method
- (NSString *)description {
    return [NSString stringWithFormat:@"TestClass: %ld", (long)self.value];
}

// Validation method without breadcrumb
- (BOOL)isValid {
    return self.value >= 0;
}

@end

// Protocol definition
@protocol TestProtocol <NSObject>
@required
- (void)requiredMethod;
@optional
- (void)optionalMethod;
@end

// Block typedef
typedef void (^CompletionBlock)(BOOL success, NSError *error);

// Function using blocks
void performAsyncOperation(CompletionBlock completion) {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // Simulate work
        BOOL success = YES;
        if (completion) {
            completion(success, nil);
        }
    });
}

// C-style function mixed with Objective-C
int calculateSum(NSArray *numbers) {
    int sum = 0;
    for (NSNumber *num in numbers) {
        sum += [num intValue];
    }
    return sum;
}

// Private method declaration
@interface TestClass ()
- (void)privateMethod;
@end

@implementation TestClass (Private)

// Private method implementation
- (void)privateMethod {
    NSLog(@"Private method called");
}

@end

// Singleton pattern
@interface SingletonClass : NSObject
+ (instancetype)sharedInstance;
- (void)doSomething;
@end

@implementation SingletonClass

+ (instancetype)sharedInstance {
    static SingletonClass *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
    });
    return instance;
}

- (void)doSomething {
    NSLog(@"Doing something");
}

@end