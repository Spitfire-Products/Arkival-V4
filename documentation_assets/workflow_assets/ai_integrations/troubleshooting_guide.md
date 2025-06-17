
# AI Integration Troubleshooting Guide

## Common API Connection Issues

### 1. Authentication Errors

#### OpenAI Authentication Issues
```
Error: "Invalid API key" or 401 Unauthorized
```

**Solutions:**
```bash
# Check API key format
echo $OPENAI_API_KEY  # Should start with "sk-proj-" or "sk-"

# Test key validity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     "https://api.openai.com/v1/models"
```

#### Google API Key Issues
```
Error: "API key not valid" or 400 Bad Request
```

**Solutions:**
```bash
# Check API key format
echo $GOOGLE_API_KEY  # Should start with "AIza"

# Verify API is enabled
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"
```

#### Common Auth Patterns Fix
```typescript
// TypeScript: Proper error handling
try {
  const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  });
  
  if (!process.env.OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY environment variable is not set');
  }
  
  if (!process.env.OPENAI_API_KEY.startsWith('sk-')) {
    throw new Error('OPENAI_API_KEY format appears invalid');
  }
} catch (error) {
  console.error('OpenAI setup error:', error.message);
}
```

### 2. Rate Limiting Issues

#### Rate Limit Error Patterns
```
OpenAI: "Rate limit exceeded" (429 status)
Google: "Quota exceeded" (429 status)
Anthropic: "rate_limit_error" (429 status)
```

#### Rate Limit Handling Implementation
```typescript
async function withRetry<T>(
  fn: () => Promise<T>, 
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && attempt < maxRetries) {
        const delay = baseDelay * Math.pow(2, attempt - 1); // Exponential backoff
        console.log(`Rate limited, retrying in ${delay}ms (attempt ${attempt})`);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}

// Usage
const result = await withRetry(() => 
  openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Hello' }]
  })
);
```

### 3. Model Availability Issues

#### Model Not Found Errors
```
OpenAI: "model_not_found" or "The model does not exist"
Google: "models/MODEL_NAME is not found"
```

#### Model Validation Function
```typescript
const VALID_MODELS = {
  openai: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
  google: ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash'],
  xai: ['grok-3-beta', 'grok-2-1212', 'grok-3-mini'],
  anthropic: ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229']
};

function validateModel(provider: string, model: string): boolean {
  const validModels = VALID_MODELS[provider];
  if (!validModels) {
    console.warn(`Unknown provider: ${provider}`);
    return false;
  }
  
  if (!validModels.includes(model)) {
    console.error(`Invalid model ${model} for provider ${provider}`);
    console.log(`Valid models: ${validModels.join(', ')}`);
    return false;
  }
  
  return true;
}
```

### 4. Network and Timeout Issues

#### Connection Timeout Errors
```typescript
// Proper timeout configuration
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  timeout: 60000, // 60 seconds
  maxRetries: 3
});

// Manual timeout wrapper
async function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Request timeout')), timeoutMs);
  });
  
  return Promise.race([promise, timeoutPromise]);
}
```

#### Proxy and Firewall Issues
```bash
# Check if corporate firewall blocks AI APIs
curl -v "https://api.openai.com/v1/models"

# Test with proxy if needed
export HTTPS_PROXY=http://your-proxy:port
export HTTP_PROXY=http://your-proxy:port
```

### 5. Library-Specific Issues

#### Google Gemini Library Issues

**Problem**: `@google/generative-ai` vs `@google/genai` confusion
```typescript
// OLD (deprecated): @google/generative-ai
import { GoogleGenerativeAI } from '@google/generative-ai';

// NEW (current): @google/genai
import { GoogleGenAI } from '@google/genai';

// Correct implementation
const ai = new GoogleGenAI({
  apiKey: process.env.GOOGLE_API_KEY
});
```

**Problem**: Image generation not working
```typescript
// WRONG: Using old text-only model
const model = ai.models.get('gemini-1.5-flash');

// CORRECT: Using image generation model
const response = await ai.models.generateContentStream({
  model: 'gemini-2.0-flash-preview-image-generation',
  config: {
    responseModalities: ['IMAGE', 'TEXT']
  },
  contents: [{ role: 'user', parts: [{ text: prompt }] }]
});
```

#### X.AI (Grok) Common Issues

**Problem**: Image generation returns URL instead of base64
```typescript
// Solution: Always request b64_json format
const response = await grokClient.images.generate({
  model: "grok-2-image-latest",
  prompt: prompt,
  response_format: "b64_json"  // Critical for consistent format
});

// Handle both possible response formats
if (response.data[0].b64_json) {
  return `data:image/jpeg;base64,${response.data[0].b64_json}`;
} else if (response.data[0].url) {
  // Fallback: convert URL to base64
  const imageResponse = await fetch(response.data[0].url);
  const imageBuffer = await imageResponse.arrayBuffer();
  const base64Data = Buffer.from(imageBuffer).toString('base64');
  return `data:image/jpeg;base64,${base64Data}`;
}
```

### 6. Parameter Compatibility Issues

#### OpenAI O-Series Model Parameters
```typescript
// WRONG: Using standard parameters for O-series models
const response = await openai.chat.completions.create({
  model: 'o1-preview',
  messages: [...],
  temperature: 0.7,  // Not supported
  max_tokens: 4096   // Should be max_completion_tokens
});

// CORRECT: O-series specific parameters
const response = await openai.chat.completions.create({
  model: 'o1-preview',
  messages: [...],
  max_completion_tokens: 4096  // Use this instead of max_tokens
  // temperature not supported for O-series
});
```

#### Provider-Specific Parameter Handling
```typescript
function getModelParams(provider: string, model: string, baseParams: any) {
  switch (provider) {
    case 'openai':
      if (model.startsWith('o1') || model.startsWith('o3')) {
        return {
          model: model,
          messages: baseParams.messages,
          max_completion_tokens: baseParams.max_tokens
          // Remove temperature, top_p for O-series
        };
      }
      return baseParams;
      
    case 'anthropic':
      return {
        ...baseParams,
        max_tokens: baseParams.max_tokens || 4096  // Required for Anthropic
      };
      
    case 'google':
      return {
        model: model,
        contents: baseParams.messages.map(msg => ({
          role: msg.role,
          parts: [{ text: msg.content }]
        }))
      };
      
    default:
      return baseParams;
  }
}
```

### 7. Response Format Issues

#### Streaming vs Non-Streaming Responses
```typescript
// Handle both streaming and non-streaming
async function handleGeminiResponse(response: any, isStreaming: boolean = false) {
  if (isStreaming) {
    for await (const chunk of response) {
      if (chunk.candidates?.[0]?.content?.parts) {
        for (const part of chunk.candidates[0].content.parts) {
          if (part.text) return part.text;
          if (part.inlineData) return `data:${part.inlineData.mimeType};base64,${part.inlineData.data}`;
        }
      }
    }
  } else {
    return response.text();
  }
}
```

#### JSON Response Parsing Issues
```typescript
// Robust JSON parsing for AI responses
function parseAIResponse(content: string): any {
  try {
    // Try direct JSON parse
    return JSON.parse(content);
  } catch (error) {
    // Try extracting JSON from markdown code blocks
    const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[1]);
    }
    
    // Try extracting JSON object
    const objectMatch = content.match(/\{[\s\S]*\}/);
    if (objectMatch) {
      return JSON.parse(objectMatch[0]);
    }
    
    throw new Error('No valid JSON found in response');
  }
}
```

### 8. Environment and Configuration Issues

#### Environment Variable Loading Issues
```typescript
// Comprehensive environment validation
function validateEnvironment(): void {
  const requiredVars = [
    'OPENAI_API_KEY',
    'GOOGLE_API_KEY'
  ];
  
  const missingVars = requiredVars.filter(varName => !process.env[varName]);
  
  if (missingVars.length > 0) {
    throw new Error(`Missing required environment variables: ${missingVars.join(', ')}`);
  }
  
  // Validate format
  if (process.env.OPENAI_API_KEY && !process.env.OPENAI_API_KEY.startsWith('sk-')) {
    console.warn('OpenAI API key format may be incorrect');
  }
  
  if (process.env.GOOGLE_API_KEY && !process.env.GOOGLE_API_KEY.startsWith('AIza')) {
    console.warn('Google API key format may be incorrect');
  }
}
```

### 9. Debugging Tools

#### API Request Logger
```typescript
class APILogger {
  static logRequest(provider: string, model: string, prompt: string) {
    console.log(`[${new Date().toISOString()}] ${provider}/${model}: ${prompt.substring(0, 100)}...`);
  }
  
  static logResponse(provider: string, responseLength: number, duration: number) {
    console.log(`[${new Date().toISOString()}] ${provider} response: ${responseLength} chars in ${duration}ms`);
  }
  
  static logError(provider: string, error: any) {
    console.error(`[${new Date().toISOString()}] ${provider} error:`, {
      message: error.message,
      status: error.status,
      code: error.code
    });
  }
}

// Usage wrapper
async function callAIWithLogging(provider: string, model: string, fn: () => Promise<string>, prompt: string) {
  const startTime = Date.now();
  APILogger.logRequest(provider, model, prompt);
  
  try {
    const result = await fn();
    APILogger.logResponse(provider, result.length, Date.now() - startTime);
    return result;
  } catch (error) {
    APILogger.logError(provider, error);
    throw error;
  }
}
```

#### Quick Diagnostic Script
```typescript
// diagnostic.ts
async function runDiagnostics() {
  console.log('🔍 AI Integration Diagnostics\n');
  
  // Environment check
  console.log('Environment Variables:');
  const envVars = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'XAI_API_KEY'];
  envVars.forEach(varName => {
    const value = process.env[varName];
    console.log(`${varName}: ${value ? '✅ Set' : '❌ Missing'}`);
  });
  
  // Network connectivity
  console.log('\nNetwork Connectivity:');
  const endpoints = [
    'https://api.openai.com',
    'https://generativelanguage.googleapis.com',
    'https://api.x.ai'
  ];
  
  for (const endpoint of endpoints) {
    try {
      const response = await fetch(endpoint, { method: 'HEAD' });
      console.log(`${endpoint}: ✅ Reachable (${response.status})`);
    } catch (error) {
      console.log(`${endpoint}: ❌ Unreachable`);
    }
  }
  
  // Model testing
  console.log('\nModel Testing:');
  const tests = [
    { provider: 'OpenAI', model: 'gpt-3.5-turbo', test: testOpenAI },
    { provider: 'Google', model: 'gemini-1.5-flash', test: testGoogle }
  ];
  
  for (const { provider, model, test } of tests) {
    try {
      await test();
      console.log(`${provider} (${model}): ✅ Working`);
    } catch (error) {
      console.log(`${provider} (${model}): ❌ Failed - ${error.message}`);
    }
  }
}

runDiagnostics();
```

This troubleshooting guide covers the most common issues encountered when integrating AI APIs across different environments and should help resolve 90% of integration problems.
