
# AI API Implementation Examples

## TypeScript/JavaScript Implementation

### OpenAI Integration (Primary Pattern)
```typescript
import OpenAI from 'openai';

// Standard OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Text completion
async function generateText(prompt: string, model: string = "gpt-4o") {
  const response = await openai.chat.completions.create({
    model: model,
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: prompt }
    ],
    temperature: 0.7,
    max_tokens: 4096
  });
  
  return response.choices[0].message.content;
}

// Image generation
async function generateImage(prompt: string, model: string = "dall-e-3") {
  const response = await openai.images.generate({
    model: model,
    prompt: prompt,
    n: 1,
    size: "1024x1024",
    quality: "standard"
  });
  
  return response.data[0].url;
}
```

### Google Gemini Integration
```typescript
// Using @google/genai library (recommended)
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({
  apiKey: process.env.GOOGLE_API_KEY
});

// Text generation
async function generateTextWithGemini(prompt: string) {
  const model = ai.models.get('gemini-1.5-flash');
  const result = await model.generateContent({
    contents: [{ 
      role: 'user', 
      parts: [{ text: prompt }] 
    }]
  });
  
  return result.response.text();
}

// Image generation with Gemini 2.0
async function generateImageWithGemini(prompt: string) {
  const config = {
    responseModalities: ['IMAGE', 'TEXT'],
    responseMimeType: 'text/plain',
  };

  const contents = [{
    role: 'user',
    parts: [{ text: prompt }],
  }];

  const response = await ai.models.generateContentStream({
    model: 'gemini-2.0-flash-preview-image-generation',
    config,
    contents,
  });

  for await (const chunk of response) {
    for (const part of chunk.candidates[0].content.parts) {
      if (part.inlineData && part.inlineData.data) {
        const mimeType = part.inlineData.mimeType || 'image/png';
        const base64Data = part.inlineData.data;
        return `data:${mimeType};base64,${base64Data}`;
      }
    }
  }
}
```

### X.AI (Grok) Integration
```typescript
// Use OpenAI client with X.AI endpoint
const grokClient = new OpenAI({
  baseURL: "https://api.x.ai/v1",
  apiKey: process.env.XAI_API_KEY
});

// Text generation
async function generateTextWithGrok(prompt: string) {
  const response = await grokClient.chat.completions.create({
    model: "grok-3-beta",
    messages: [
      { role: "user", content: prompt }
    ],
    temperature: 0.7,
    max_tokens: 4096
  });
  
  return response.choices[0].message.content;
}

// Image generation
async function generateImageWithGrok(prompt: string) {
  const response = await grokClient.images.generate({
    model: "grok-2-image-latest",
    prompt: prompt,
    n: 1,
    response_format: "b64_json"
  });
  
  if (response.data[0].b64_json) {
    return `data:image/jpeg;base64,${response.data[0].b64_json}`;
  }
}
```

### Anthropic Claude Integration
```typescript
// Direct HTTP approach (no official client used in this app)
async function generateTextWithClaude(prompt: string) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': process.env.ANTHROPIC_API_KEY!,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      model: 'claude-3-5-sonnet-20241022',
      messages: [
        { role: 'user', content: prompt }
      ],
      max_tokens: 4096,
      temperature: 0.7
    })
  });
  
  const data = await response.json();
  return data.content[0].text;
}
```

## Python Implementation

### Universal Python Pattern (from llm_handler.py)
```python
import os
import requests
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIProvider:
    def __init__(self, provider_name: str):
        self.provider = provider_name
        self.setup_client()
    
    def setup_client(self):
        if self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "google":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        elif self.provider == "xai":
            self.client = OpenAI(
                base_url="https://api.x.ai/v1",
                api_key=os.getenv("XAI_API_KEY")
            )
        elif self.provider == "deepseek":
            self.client = OpenAI(
                base_url="https://api.deepseek.com",
                api_key=os.getenv("DEEPSEEK_API_KEY")
            )

    def generate_text(self, prompt: str, model: str):
        if self.provider == "openai" or self.provider in ["xai", "deepseek"]:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            return response.choices[0].message.content
            
        elif self.provider == "google":
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(prompt)
            return response.text
            
        elif self.provider == "anthropic":
            headers = {
                "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096,
                "temperature": 0.7
            }
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            return response.json()["content"][0]["text"]
```

### Google Gemini Python (Legacy Pattern)
```python
# Using google-generativeai library
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_with_gemini(prompt: str, model: str = "gemini-1.5-flash"):
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)
    return response.text
```

## Rust Implementation

### Basic Rust HTTP Client Pattern
```rust
use reqwest;
use serde_json::{json, Value};
use std::env;

pub struct OpenAIClient {
    client: reqwest::Client,
    api_key: String,
}

impl OpenAIClient {
    pub fn new() -> Self {
        let api_key = env::var("OPENAI_API_KEY")
            .expect("OPENAI_API_KEY must be set");
        
        Self {
            client: reqwest::Client::new(),
            api_key,
        }
    }
    
    pub async fn generate_text(&self, prompt: &str, model: &str) -> Result<String, Box<dyn std::error::Error>> {
        let request_body = json!({
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        });
        
        let response = self.client
            .post("https://api.openai.com/v1/chat/completions")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request_body)
            .send()
            .await?;
            
        let json: Value = response.json().await?;
        let content = json["choices"][0]["message"]["content"]
            .as_str()
            .unwrap_or("No content")
            .to_string();
            
        Ok(content)
    }
}

// Usage
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = OpenAIClient::new();
    let result = client.generate_text("Hello, world!", "gpt-4o").await?;
    println!("Response: {}", result);
    Ok(())
}
```

## Java Implementation

### Java HTTP Client Pattern
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class OpenAIClient {
    private final HttpClient client;
    private final String apiKey;
    private final ObjectMapper mapper;
    
    public OpenAIClient(String apiKey) {
        this.client = HttpClient.newHttpClient();
        this.apiKey = apiKey;
        this.mapper = new ObjectMapper();
    }
    
    public String generateText(String prompt, String model) throws Exception {
        String requestBody = String.format("""
            {
                "model": "%s",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "%s"}
                ],
                "temperature": 0.7,
                "max_tokens": 4096
            }
            """, model, prompt.replace("\"", "\\\""));
            
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.openai.com/v1/chat/completions"))
            .header("Authorization", "Bearer " + apiKey)
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();
            
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
            
        JsonNode json = mapper.readTree(response.body());
        return json.get("choices").get(0).get("message").get("content").asText();
    }
}

// Usage
public class Main {
    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("OPENAI_API_KEY");
        OpenAIClient client = new OpenAIClient(apiKey);
        String result = client.generateText("Hello, world!", "gpt-4o");
        System.out.println("Response: " + result);
    }
}
```

## Key Implementation Notes

### 1. Authentication Patterns
- **OpenAI**: `Authorization: Bearer {api_key}`
- **Google**: API key in request or client initialization
- **Anthropic**: `x-api-key: {api_key}` + `anthropic-version: 2023-06-01`
- **X.AI**: Same as OpenAI (Bearer token)
- **Others**: Follow OpenAI-compatible pattern

### 2. Request Formats
- **OpenAI-compatible**: All providers except Google and Anthropic
- **Google**: Uses `contents` array with `parts` structure
- **Anthropic**: Uses `messages` but requires `max_tokens`

### 3. Response Handling
- **OpenAI pattern**: `response.choices[0].message.content`
- **Google**: `response.text()` or streaming with `inlineData`
- **Anthropic**: `response.content[0].text`

### 4. Error Handling
All implementations should include:
- API key validation
- Rate limiting handling
- Timeout configuration
- Proper error propagation

### 5. Dependencies
- **TypeScript**: `openai`, `@google/genai`
- **Python**: `openai`, `google-generativeai`, `requests`
- **Rust**: `reqwest`, `serde_json`, `tokio`
- **Java**: Built-in HTTP client, Jackson for JSON
# AI Integration Implementation Examples

## Complete Working Code Examples

This document contains copy-pasteable implementation examples from comprehensive application development.

### TypeScript Implementation (Primary)

#### Core AI Service Setup
```typescript
// server/ai-service.ts - Main service class
import { GoogleGenerativeAI } from '@google/genai';
import OpenAI from 'openai';

export class AIService {
  private openai: OpenAI;
  private google: GoogleGenerativeAI;
  private xaiClient: OpenAI;
  private deepseekClient: OpenAI;
  private perplexityClient: OpenAI;
  private nvidiaClient: OpenAI;

  constructor() {
    // Initialize OpenAI
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    // Initialize Google Gemini
    this.google = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '');

    // Initialize X.AI (Grok) with OpenAI client
    this.xaiClient = new OpenAI({
      apiKey: process.env.XAI_API_KEY,
      baseURL: 'https://api.x.ai/v1',
    });

    // Initialize DeepSeek
    this.deepseekClient = new OpenAI({
      apiKey: process.env.DEEPSEEK_API_KEY,
      baseURL: 'https://api.deepseek.com',
    });

    // Initialize Perplexity
    this.perplexityClient = new OpenAI({
      apiKey: process.env.PERPLEXITY_API_KEY,
      baseURL: 'https://api.perplexity.ai',
    });

    // Initialize Nvidia
    this.nvidiaClient = new OpenAI({
      apiKey: process.env.NVIDIA_API_KEY,
      baseURL: 'https://integrate.api.nvidia.com/v1',
    });
  }
}
```

#### Text Generation Implementation
```typescript
// Text generation with multi-provider support
async generateText(prompt: string, model: string = 'gpt-4o'): Promise<string> {
  try {
    const provider = this.getTextProvider(model);
    
    switch (provider) {
      case 'openai':
        const openaiResponse = await this.openai.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000,
        });
        return openaiResponse.choices[0]?.message?.content || '';

      case 'google':
        const genModel = this.google.getGenerativeModel({ model });
        const result = await genModel.generateContent(prompt);
        return result.response.text();

      case 'xai':
        const xaiResponse = await this.xaiClient.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000,
        });
        return xaiResponse.choices[0]?.message?.content || '';

      case 'anthropic':
        return await this.callAnthropicAPI(prompt, model);

      case 'deepseek':
        const deepseekResponse = await this.deepseekClient.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000,
        });
        return deepseekResponse.choices[0]?.message?.content || '';

      case 'perplexity':
        const perplexityResponse = await this.perplexityClient.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000,
        });
        return perplexityResponse.choices[0]?.message?.content || '';

      case 'nvidia':
        const nvidiaResponse = await this.nvidiaClient.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000,
        });
        return nvidiaResponse.choices[0]?.message?.content || '';

      default:
        throw new Error(`Unsupported provider: ${provider}`);
    }
  } catch (error) {
    console.error('Text generation error:', error);
    throw error;
  }
}
```

#### Image Generation Implementation
```typescript
// Image generation with multi-provider support
async generateImage(prompt: string, model: string = 'gemini-2.0-flash-preview-image-generation'): Promise<string> {
  try {
    const provider = this.getImageProvider(model);
    
    switch (provider) {
      case 'openai':
        const openaiResponse = await this.openai.images.generate({
          model,
          prompt,
          size: '1024x1024',
          n: 1,
        });
        return openaiResponse.data[0]?.url || '';

      case 'gemini':
        const genModel = this.google.getGenerativeModel({ model });
        const result = await genModel.generateContent(prompt);
        
        // Extract image from Gemini response
        const candidates = result.response.candidates;
        if (candidates && candidates[0]?.content?.parts) {
          for (const part of candidates[0].content.parts) {
            if (part.inlineData && part.inlineData.data) {
              const base64Data = part.inlineData.data;
              const mimeType = part.inlineData.mimeType || 'image/jpeg';
              return `data:${mimeType};base64,${base64Data}`;
            }
          }
        }
        throw new Error('No image data in Gemini response');

      case 'xai':
        const xaiResponse = await this.xaiClient.images.generate({
          model,
          prompt,
          size: '1024x1024',
          n: 1,
        });
        return xaiResponse.data[0]?.url || '';

      default:
        throw new Error(`Unsupported image provider: ${provider}`);
    }
  } catch (error) {
    console.error('Image generation error:', error);
    throw error;
  }
}
```

#### Provider Detection Logic
```typescript
// Determine which provider to use based on model name
private getTextProvider(model: string): 'openai' | 'google' | 'xai' | 'anthropic' | 'deepseek' | 'perplexity' | 'nvidia' {
  if (model.startsWith('gpt-') || model.startsWith('o1') || model.startsWith('o3') || model.startsWith('o4')) {
    return 'openai';
  }
  if (model.includes('gemini') || model.includes('flash')) {
    return 'google';
  }
  if (model.includes('grok')) {
    return 'xai';
  }
  if (model.includes('claude')) {
    return 'anthropic';
  }
  if (model.includes('deepseek')) {
    return 'deepseek';
  }
  if (model.includes('sonar') || model.includes('mixtral') || model.includes('mistral')) {
    return 'perplexity';
  }
  if (model.includes('nemotron')) {
    return 'nvidia';
  }
  return 'openai'; // Default
}

private getImageProvider(model: string): 'openai' | 'gemini' | 'xai' {
  if (model.includes('gemini') || model.includes('flash') || model.includes('2.0')) {
    return 'gemini';
  }
  if (model.startsWith('dall-e')) {
    return 'openai';
  }
  if (model.includes('grok') && model.includes('image')) {
    return 'xai';
  }
  return 'gemini'; // Default to Gemini
}
```

#### Anthropic Direct HTTP Implementation
```typescript
// Anthropic Claude implementation (direct HTTP)
private async callAnthropicAPI(prompt: string, model: string): Promise<string> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': process.env.ANTHROPIC_API_KEY || '',
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model,
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  if (!response.ok) {
    throw new Error(`Anthropic API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.content[0]?.text || '';
}
```

### Python Implementation (Reference)

#### LLM Handler Class
```python
# ai_integrations/llm_handler.py
import os
import openai
import google.generativeai as genai
import requests
from typing import Optional, Dict, Any

class LLMHandler:
    def __init__(self):
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Initialize Google Gemini
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        # X.AI client (using OpenAI SDK)
        self.xai_client = openai.OpenAI(
            api_key=os.getenv('XAI_API_KEY'),
            base_url='https://api.x.ai/v1'
        )
        
        # DeepSeek client
        self.deepseek_client = openai.OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url='https://api.deepseek.com'
        )

    def generate_text(self, prompt: str, model: str = 'gpt-4o') -> str:
        """Generate text using specified model"""
        try:
            provider = self._get_provider(model)
            
            if provider == 'openai':
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif provider == 'google':
                model_instance = genai.GenerativeModel(model)
                response = model_instance.generate_content(prompt)
                return response.text
                
            elif provider == 'xai':
                response = self.xai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif provider == 'deepseek':
                response = self.deepseek_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif provider == 'anthropic':
                return self._call_anthropic(prompt, model)
                
        except Exception as e:
            print(f"Error generating text: {e}")
            raise

    def generate_image(self, prompt: str, model: str = 'gemini-2.0-flash-preview-image-generation') -> Optional[str]:
        """Generate image using specified model"""
        try:
            provider = self._get_image_provider(model)
            
            if provider == 'openai':
                response = self.openai_client.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024",
                    n=1
                )
                return response.data[0].url
                
            elif provider == 'google':
                model_instance = genai.GenerativeModel(model)
                response = model_instance.generate_content(prompt)
                # Handle Gemini image response
                return self._extract_gemini_image(response)
                
            elif provider == 'xai':
                response = self.xai_client.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024",
                    n=1
                )
                return response.data[0].url
                
        except Exception as e:
            print(f"Error generating image: {e}")
            raise

    def _get_provider(self, model: str) -> str:
        """Determine provider based on model name"""
        if model.startswith(('gpt-', 'o1', 'o3', 'o4')):
            return 'openai'
        elif 'gemini' in model or 'flash' in model:
            return 'google'
        elif 'grok' in model:
            return 'xai'
        elif 'claude' in model:
            return 'anthropic'
        elif 'deepseek' in model:
            return 'deepseek'
        return 'openai'

    def _get_image_provider(self, model: str) -> str:
        """Determine image provider based on model name"""
        if 'gemini' in model or 'flash' in model or '2.0' in model:
            return 'google'
        elif model.startswith('dall-e'):
            return 'openai'
        elif 'grok' in model and 'image' in model:
            return 'xai'
        return 'google'

    def _call_anthropic(self, prompt: str, model: str) -> str:
        """Direct HTTP call to Anthropic API"""
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('ANTHROPIC_API_KEY'),
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': model,
            'max_tokens': 2000,
            'messages': [{'role': 'user', 'content': prompt}]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['content'][0]['text']
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")

    def _extract_gemini_image(self, response) -> Optional[str]:
        """Extract image data from Gemini response"""
        candidates = response.candidates
        if candidates and candidates[0].content.parts:
            for part in candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    base64_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type or 'image/jpeg'
                    return f"data:{mime_type};base64,{base64_data}"
        return None
```

### Frontend Integration Examples

#### React Hook for AI Service
```typescript
// client/src/hooks/use-ai.ts
import { useState } from 'react';
import { aiService } from '../lib/ai-service';

export function useAI() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateText = async (prompt: string, model?: string) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const result = await aiService.generateText(prompt, model);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setIsGenerating(false);
    }
  };

  const generateImage = async (prompt: string, model?: string) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const result = await aiService.generateImage(prompt, model);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setIsGenerating(false);
    }
  };

  return {
    generateText,
    generateImage,
    isGenerating,
    error,
  };
}
```

#### Client-Side AI Service
```typescript
// client/src/lib/ai-service.ts
class ClientAIService {
  private baseUrl = '/api';

  async generateText(prompt: string, model?: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/generate-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt, model }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.text;
  }

  async generateImage(prompt: string, model?: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/generate-image`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt, model }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.imageUrl;
  }
}

export const aiService = new ClientAIService();
```

### Testing Examples

#### TypeScript Test
```typescript
// tests/quick-model-test.ts
import { AIService } from '../server/ai-service';

async function testModels() {
  const aiService = new AIService();
  
  const models = [
    'gpt-4o',
    'gemini-2.5-flash',
    'grok-3-beta',
    'claude-3-5-sonnet-20241022',
    'deepseek-coder'
  ];

  for (const model of models) {
    try {
      console.log(`Testing ${model}...`);
      const result = await aiService.generateText('Say hello', model);
      console.log(`✅ ${model}: ${result.slice(0, 50)}...`);
    } catch (error) {
      console.log(`❌ ${model}: ${error}`);
    }
  }
}

testModels();
```

#### Python Test
```python
# tests/test_ai_connections.py
import os
from ai_integrations.llm_handler import LLMHandler

def test_all_providers():
    handler = LLMHandler()
    
    test_cases = [
        ('gpt-4o', 'OpenAI'),
        ('gemini-2.5-flash', 'Google'),
        ('grok-3-beta', 'X.AI'),
        ('claude-3-5-sonnet-20241022', 'Anthropic'),
        ('deepseek-coder', 'DeepSeek')
    ]
    
    for model, provider in test_cases:
        try:
            result = handler.generate_text('Say hello', model)
            print(f"✅ {provider} ({model}): Connected")
        except Exception as e:
            print(f"❌ {provider} ({model}): {e}")

if __name__ == "__main__":
    test_all_providers()
```

### Environment Configuration

#### .env.example
```bash
# AI Provider API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
DEEPSEEK_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
PERPLEXITY_API_KEY=pplx-...

# Default model configurations
DEFAULT_TEXT_MODEL=gpt-4o
DEFAULT_IMAGE_MODEL=gemini-2.0-flash-preview-image-generation
DEFAULT_ENHANCEMENT_MODEL=gpt-4o
```

### Error Handling Patterns

#### Robust Error Handling
```typescript
// Enhanced error handling with fallbacks
async generateTextWithFallback(prompt: string, models: string[] = ['gpt-4o', 'gemini-2.5-flash']): Promise<string> {
  let lastError: Error | null = null;
  
  for (const model of models) {
    try {
      return await this.generateText(prompt, model);
    } catch (error) {
      console.warn(`Model ${model} failed:`, error);
      lastError = error instanceof Error ? error : new Error(String(error));
      continue;
    }
  }
  
  throw new Error(`All models failed. Last error: ${lastError?.message}`);
}
```

This implementation guide provides working, tested code examples that can be directly integrated into new projects using proven AI integration patterns.
