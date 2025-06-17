
# AI API Integration Reference Guide

## Overview

This guide provides comprehensive information for integrating multiple AI service providers across different programming languages and frameworks. It includes working model names, API endpoints, authentication patterns, and implementation examples.

## Supported AI Providers

### 1. OpenAI
- **Endpoint**: `https://api.openai.com/v1`
- **Authentication**: Bearer token via `Authorization` header
- **Environment Variable**: `OPENAI_API_KEY`

**Working Models (2024-2025)**:
```
Text Generation:
- gpt-4o (latest, recommended)
- gpt-4o-mini
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo
- o1, o1-mini, o1-preview, o1-pro
- o3, o3-mini
- o4-mini

Image Generation:
- dall-e-3 (recommended)
- dall-e-2

Audio/Speech:
- whisper-1 (speech-to-text)
- tts-1, tts-1-hd (text-to-speech)

Embeddings:
- text-embedding-3-large
- text-embedding-3-small
- text-embedding-ada-002
```

### 2. Google Gemini
- **Endpoint**: `https://generativelanguage.googleapis.com`
- **Authentication**: API key via `x-goog-api-key` header or query parameter
- **Environment Variable**: `GOOGLE_API_KEY`

**Working Models (2024-2025)**:
```
Latest Generation:
- gemini-2.5-flash-preview-05-20 (latest)
- gemini-2.5-flash-preview-04-17
- gemini-2.5-pro-preview-03-25

Gemini 2.0 Series:
- gemini-2.0-flash
- gemini-2.0-flash-001
- gemini-2.0-flash-exp-image-generation
- gemini-2.0-flash-preview-image-generation (primary image model)
- gemini-2.0-flash-lite

Gemini 1.5 Series:
- gemini-1.5-pro
- gemini-1.5-flash
- gemini-1.5-flash-latest
- gemini-1.5-pro-latest

Legacy/Specialized:
- gemini-pro-vision
- gemini-ultra
- gemini-pro (legacy)

Gemma Models:
- gemma-7b
- gemma-2b
- gemma-3-1b-it
```

### 3. Anthropic Claude
- **Endpoint**: `https://api.anthropic.com`
- **Authentication**: API key via `x-api-key` header
- **Environment Variable**: `ANTHROPIC_API_KEY`
- **Required Header**: `anthropic-version: 2023-06-01`

**Working Models**:
```
Claude 3.5 Series:
- claude-3-5-sonnet-20241022 (latest, recommended)

Claude 3 Series:
- claude-3-opus-20240229 (most capable)
- claude-3-sonnet-20240229 (balanced)
- claude-3-haiku-20240307 (fastest)

Legacy:
- claude-2
- claude-instant-1
```

### 4. X.AI (Grok)
- **Endpoint**: `https://api.x.ai/v1`
- **Authentication**: Bearer token via `Authorization` header
- **Environment Variable**: `XAI_API_KEY`

**Working Models**:
```
Grok 3 Series:
- grok-3-beta (latest)
- grok-3-mini-beta
- grok-3-fast-beta
- grok-3-mini-fast-beta

Grok 2 Series:
- grok-2-1212 (text)
- grok-2-vision-1212 (vision)
- grok-2-image-1212 (image generation)
- grok-2-image-latest (latest image model)

Legacy:
- grok-beta
- grok-vision-beta
```

### 5. DeepSeek
- **Endpoint**: `https://api.deepseek.com`
- **Authentication**: Bearer token via `Authorization` header
- **Environment Variable**: `DEEPSEEK_API_KEY`

**Working Models**:
```
- deepseek-chat (general purpose)
- deepseek-reasoner (reasoning-specialized)
- deepseek-coder (code-specialized, recommended)
```

### 6. Nvidia Nemotron
- **Endpoint**: `https://integrate.api.nvidia.com/v1`
- **Authentication**: Bearer token via `Authorization` header
- **Environment Variable**: `NVIDIA_API_KEY`

**Working Models**:
```
- nemotron-4-340b (ultra large, latest)
- nemotron-4-midi (mid-sized)
- nemotron-4-mini (smaller, faster)
- nemotron-3-8b (smaller 8B model)
```

### 7. Perplexity AI
- **Endpoint**: `https://api.perplexity.ai`
- **Authentication**: Bearer token via `Authorization` header
- **Environment Variable**: `PERPLEXITY_API_KEY`

**Working Models**:
```
Online Search Models:
- llama-3.1-sonar-small-128k-online (recommended)
- llama-3.1-sonar-large-128k-online
- llama-3.1-sonar-huge-128k-online

Chat Models (no search):
- sonar-small-chat
- sonar-medium-chat
- sonar-large-chat
- mixtral-8x7b-instruct
- mistral-7b-instruct
```

## Implementation Patterns

### TypeScript/Node.js Implementation

#### Using OpenAI Client Library
```typescript
import OpenAI from 'openai';

// Initialize client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Text generation
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' }
  ],
  temperature: 0.7,
  max_tokens: 1000
});

// Image generation
const imageResponse = await openai.images.generate({
  model: 'dall-e-3',
  prompt: 'A futuristic cityscape',
  size: '1024x1024',
  quality: 'standard'
});
```

#### Using OpenAI Client for Other Providers
```typescript
// DeepSeek
const deepseekClient = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: 'https://api.deepseek.com'
});

// X.AI (Grok)
const grokClient = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1'
});

// Nvidia
const nvidiaClient = new OpenAI({
  apiKey: process.env.NVIDIA_API_KEY,
  baseURL: 'https://integrate.api.nvidia.com/v1'
});
```

#### Google Gemini with Official Library
```typescript
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

const result = await model.generateContent('Hello world');
```

#### Google Gemini Image Generation (New SDK)
```typescript
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({
  apiKey: process.env.GOOGLE_API_KEY!
});

const response = await ai.models.generateContentStream({
  model: 'gemini-2.0-flash-preview-image-generation',
  config: {
    responseModalities: ['IMAGE', 'TEXT']
  },
  contents: [{
    role: 'user',
    parts: [{ text: 'Generate an image of a sunset' }]
  }]
});
```

#### Anthropic Claude
```typescript
const response = await fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {
    'x-api-key': process.env.ANTHROPIC_API_KEY!,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json'
  },
  body: JSON.stringify({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 1000,
    messages: [
      { role: 'user', content: 'Hello!' }
    ]
  })
});
```

### Python Implementation

#### Using OpenAI Client
```python
import openai
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Text generation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)
```

#### Google Gemini in Python
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello world")
```

#### Using Requests for HTTP Calls
```python
import requests

# Anthropic Claude
headers = {
    "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

data = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "Hello!"}]
}

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers=headers,
    json=data
)
```

## Required Dependencies

### TypeScript/Node.js
```json
{
  "dependencies": {
    "openai": "^4.x.x",
    "@google/generative-ai": "^0.x.x",
    "@google/genai": "^0.x.x"
  },
  "devDependencies": {
    "@types/node": "^20.x.x",
    "tsx": "^4.x.x"
  }
}
```

### Python
```txt
openai>=1.0.0
google-generativeai>=0.3.0
requests>=2.28.0
python-dotenv>=1.0.0
```

## Error Handling Best Practices

### Rate Limiting
```typescript
async function retryWithBackoff(fn: () => Promise<any>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

### API Key Validation
```typescript
function validateApiKeys() {
  const requiredKeys = [
    'OPENAI_API_KEY',
    'GOOGLE_API_KEY',
    'ANTHROPIC_API_KEY',
    'XAI_API_KEY',
    'DEEPSEEK_API_KEY'
  ];

  const missing = requiredKeys.filter(key => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(`Missing API keys: ${missing.join(', ')}`);
  }
}
```

## Environment Variables Template

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic Claude API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# X.AI (Grok) API Configuration
XAI_API_KEY=your_xai_api_key_here

# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Nvidia API Configuration
NVIDIA_API_KEY=your_nvidia_api_key_here

# Perplexity API Configuration
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

## Common Issues and Solutions

### 1. Model Not Found Errors
- Always use exact model names from the working models list
- Check for typos in model names
- Verify the model is available in your region

### 2. Authentication Failures
- Ensure API keys are correctly set in environment variables
- Check for leading/trailing spaces in API keys
- Verify the correct header format for each provider

### 3. Rate Limiting
- Implement exponential backoff retry logic
- Use appropriate delay between requests
- Consider using lower-tier models for development

### 4. Response Format Issues
- Different providers return different response structures
- Always check for null/undefined responses
- Implement proper error handling for each provider

### 5. Image Generation Specifics
- Gemini requires the new `@google/genai` library for image generation
- X.AI Grok image models return base64 format when using `response_format: "b64_json"`
- DALL-E has specific size requirements

## Provider-Specific Notes

### OpenAI
- O-series models (o1, o3, o4) use `max_completion_tokens` instead of `max_tokens`
- O-series models may not support all parameters (temperature, etc.)
- GPT-4o series also uses `max_completion_tokens`

### Google Gemini
- Use `@google/generative-ai` for text generation
- Use `@google/genai` for image generation with 2.0 models
- Image generation requires `responseModalities: ['IMAGE', 'TEXT']`

### X.AI (Grok)
- Supports both text and image generation
- Image models work best with `response_format: "b64_json"`
- Some models may not support frequency_penalty/presence_penalty

### Anthropic Claude
- Requires `anthropic-version` header
- `max_tokens` parameter is required
- Different message format compared to OpenAI

### Perplexity
- Online models provide search capabilities
- Different default parameters (temperature: 0.2, top_p: 0.9)
- May include citations in responses

This guide should be updated as new models and API versions become available.
