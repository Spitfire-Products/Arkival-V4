// JavaScript test functions for breadcrumb detection validation

function basicFunction() {
    return "test";
}

const arrowFunction = (param1, param2 = "default") => {
    return `${param1}_${param2}`;
};

// Function without breadcrumb documentation
function undocumentedFunction() {
    return "no breadcrumb";
}

async function asyncFunction(data) {
    return Object.keys(data);
}

const functionExpression = function(value) {
    return Boolean(value);
};

function multiLineCommentFunction(x, y) {
    return x + y;
}

function* generatorFunction(items) {
    for (const item of items) {
        yield item.toUpperCase();
    }
}

class TestClass {
    documentedMethod(value) {
        return Boolean(value);
    }
    
    undocumentedMethod() {
        // Method without breadcrumb
        return null;
    }
    
    static staticMethod(x, y) {
        return x + y;
    }
    
    async asyncMethod(data) {
        return await Promise.resolve(data);
    }
}

function higherOrderFunction(callback) {
    return function(data) {
        return callback(data.toString());
    };
}

function restParametersFunction(first, ...rest) {
    return [first, ...rest];
}

function exportedFunction(data) {
    return JSON.stringify(data);
}