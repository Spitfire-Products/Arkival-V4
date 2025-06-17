# AI Model Provider Reference

## Complete Model Inventory

This reference contains all working AI models from the comprehensive application testing, including current implementations and legacy configurations.

### OpenAI Models
**Status**: ✅ Currently Active  
**Implementation**: TypeScript (server/ai-service.ts), Python (ai_integrations/llm_handler.py)

```javascript
// Current working models
const openaiModels = {
  // Latest GPT-4 Series
  "gpt-4o": "Primary text model (May 2024)",
  "gpt-4o-mini": "Faster, smaller GPT-4o",
  "gpt-4-turbo": "GPT-4 turbo version",
  "gpt-4": "Standard GPT-4",

  // O-Series (Reasoning)
  "o1": "O1 reasoning model",
  "o1-mini": "Smaller O1 model", 
  "o1-preview": "O1 preview version",
  "o1-pro": "O1 professional version",
  "o3": "Latest O3 model",
  "o3-mini": "Smaller O3 model",
  "o4-mini": "O4 mini model",

  // Legacy
  "gpt-3.5-turbo": "Legacy but still working",

  // Image Generation
  "dall-e-3": "Primary image model",
  "dall-e-2": "Legacy image model",

  // Audio/Speech
  "whisper-1": "Speech-to-text",
  "tts-1": "Text-to-speech",
  "tts-1-hd": "High-quality TTS",

  // Embeddings
  "text-embedding-3-large": "Large embeddings",
  "text-embedding-3-small": "Small embeddings",
  "text-embedding-ada-002": "Legacy embeddings"
};
```

### Google Gemini Models
**Status**: ✅ Currently Active (Primary Image Provider)  
**Implementation**: TypeScript (@google/genai), Python (google.generativeai)

```javascript
const geminiModels = {
  // Gemini 2.5 Series (Latest)
  "gemini-2.5-flash-preview-04-17": "Latest Gemini 2.5",
  "gemini-2.5-pro-preview-03-25": "Gemini 2.5 Pro",

  // Gemini 2.0 Series 
  "gemini-2.0-flash": "Gemini 2.0 Flash",
  "gemini-2.0-flash-preview-image-generation": "Primary image model",
  "gemini-2.0-flash-exp-image-generation": "Experimental image",
  "gemini-2.0-flash-lite": "Lightweight version",

  // Gemini 1.5 Series
  "gemini-1.5-pro": "Gemini 1.5 Pro",
  "gemini-1.5-flash": "Fast Gemini 1.5",
  "gemini-1.5-pro-latest": "Latest Pro version",
  "gemini-1.5-flash-latest": "Latest Flash version",

  // Gemma 3 Series (FREE - Prompt Enhancement)
  "gemma-3-1b-it": "Gemma 3 1B (FREE) - Primary prompt enhancement",
  "gemma-3-4b-it": "Gemma 3 4B (FREE) - Enhanced prompt quality",
  "gemma-3-12b-it": "Gemma 3 12B (FREE) - High-quality enhancement (default)",
  "gemma-3-27b-it": "Gemma 3 27B (FREE) - Premium prompt enhancement",
  "gemma-3n-e4b-it": "Gemma 3N E4B (FREE) - Specialized variant",

  // Legacy
  "gemini-pro-vision": "Vision capabilities",
  "gemini-pro": "Legacy Gemini Pro",
  "gemini-ultra": "Ultra model"
};
```

### X.AI (Grok) Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with X.AI endpoint

```javascript
const xaiModels = {
  // Grok 3 Series (Latest)
  "grok-3-beta": "Latest Grok 3",
  "grok-3-mini": "Smaller Grok 3",
  "grok-3-fast-beta": "Fast Grok 3",
  "grok-3-mini-fast-beta": "Mini fast version",

  // Grok 2 Series
  "grok-2-1212": "Grok 2 text model",
  "grok-2-vision-1212": "Grok 2 vision",
  "grok-2-image-1212": "Grok 2 image generation",
  "grok-2-image-latest": "Latest image model",

  // Legacy
  "grok-beta": "Legacy Grok beta",
  "grok-vision-beta": "Legacy vision beta"
};
```

### Anthropic Claude Models
**Status**: ✅ Currently Active  
**Implementation**: Direct HTTP requests

```javascript
const anthropicModels = {
  "claude-3-5-sonnet-20241022": "Latest Claude 3.5 (Oct 2024)",
  "claude-3-opus-20240229": "Most capable Claude 3",
  "claude-3-sonnet-20240229": "Balanced Claude 3",
  "claude-3-haiku-20240307": "Fastest Claude 3",
  "claude-2": "Legacy Claude 2",
  "claude-instant-1": "Fast legacy model"
};
```

### DeepSeek Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with DeepSeek endpoint

```javascript
const deepseekModels = {
  "deepseek-chat": "General purpose",
  "deepseek-reasoner": "Reasoning specialized",
  "deepseek-coder": "Code specialized (recommended)"
};
```

### Nvidia Nemotron Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with Nvidia endpoint

```javascript
const nvidiaModels = {
  "nemotron-4-340b": "Ultra large 340B model",
  "nemotron-4-midi": "Mid-sized model",
  "nemotron-4-mini": "Smaller, faster model",
  "nemotron-3-8b": "8B parameter model"
};
```

### Perplexity Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with Perplexity endpoint

```javascript
const perplexityModels = {
  "llama-3.1-sonar-large-128k-online": "Large with web search",
  "llama-3.1-sonar-small-128k-online": "Small with web search",
  "sonar-large-chat": "Large without search",
  "sonar-small-chat": "Small without search",
  "mixtral-8x7b-instruct": "Mixtral 8x7B",
  "mistral-7b-instruct": "Mistral 7B"
};
```

### NVIDIA NIM Models
**Status**: ✅ Working - Via X.AI API Gateway
**API Base**: `https://integrate.api.nvidia.com/v1`
**Models Available**:
- `nvidia/llama-3.1-nemotron-70b-instruct` - ✅ Working
- `meta/llama-3.1-8b-instruct` - ✅ Working  
- `meta/llama-3.1-70b-instruct` - ✅ Working
- `microsoft/phi-3-mini-128k-instruct` - ✅ Working
- `google/gemma-2-9b-it` - ✅ Working for text tasks
- `google/gemma-2-27b-it` - ✅ Working for text tasks

### Google Gemma-3 Models (via NVIDIA)
**Status**: ✅ Working - Specialized for prompt enhancement
**API Base**: `https://integrate.api.nvidia.com/v1`
**Models Available**:
- `google/gemma-3-8b-it` - ✅ Working - **Used for prompt enhancement**
- `google/gemma-3-2b-it` - ✅ Working - Lightweight option
- `google/gemma-3-27b-it` - ✅ Working - High-performance option

**Special Use Case**: These Gemma-3 models are specifically configured in our enhance prompt functions for improving user prompts before sending to image generation models.

## API Endpoint Configuration

### Environment Variables Required
```bash
# Primary providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
DEEPSEEK_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
PERPLEXITY_API_KEY=pplx-...
```

### Provider Endpoints
```javascript
const endpoints = {
  openai: "https://api.openai.com/v1",
  google: "https://generativelanguage.googleapis.com",
  anthropic: "https://api.anthropic.com",
  xai: "https://api.x.ai/v1",
  deepseek: "https://api.deepseek.com",
  nvidia: "https://integrate.api.nvidia.com/v1",
  perplexity: "https://api.perplexity.ai"
};
```

## Working Model Status Matrix

| Provider | Text Generation | Image Generation | Prompt Enhancement | Image Editing | Status |
|----------|----------------|------------------|-------------------|---------------|---------|
| OpenAI | ✅ gpt-4o | ✅ dall-e-3 | ✅ gpt-4o-mini | ❌ | Active |
| Google | ✅ gemini-2.5-flash | ✅ gemini-2.0-flash-preview | ✅ **gemma-3-12b-it (FREE)** | ✅ | Primary |
| X.AI | ✅ grok-3-beta | ✅ grok-2-image-latest | ✅ grok-2-1212 | ✅ (via Gemini) | Active |
| Anthropic | ✅ claude-3-5-sonnet | ❌ | ✅ claude-3-5-sonnet | ❌ | Active |
| DeepSeek | ✅ deepseek-coder | ❌ | ✅ deepseek-chat | ❌ | Active |
| Nvidia | ✅ nemotron-4-340b | ❌ | ❌ | ❌ | Active |
| Perplexity | ✅ llama-3.1-sonar | ❌ | ❌ | ❌ | Active |

## Deprecated/Removed Models
```javascript
// These models were removed or are no longer working
const deprecatedModels = {
  "gemma-3-1b-it": "Not implemented in LLMModelMapper",
  "gemma-7b": "Removed from working implementation", 
  "gemma-2b": "Removed from working implementation",
  "gpt-4.1": "Listed in llm_handler.py but not verified working",
  "gpt-4.1-mini": "Listed in llm_handler.py but not verified working"
};
```

## Integration Notes

### Current Primary Configuration
- **Text Generation**: OpenAI gpt-4o (default), user-configurable
- **Image Generation**: Google Gemini 2.0 Flash Preview (primary)
- **Image Editing**: Google Gemini (all editing routes through Gemini)
- **Prompt Enhancement**: **Gemma-3-12b-it (FREE)** as default, user-configurable

### Free Model Advantages
- **Gemma-3 Series**: Completely FREE models via Google API
- **No API costs**: Perfect for prompt enhancement without usage charges
- **High quality**: Gemma-3-12b-it provides excellent prompt enhancement
- **Multiple sizes**: Choose based on speed vs quality preferences
```typescript
// From server/ai-service.ts
function getImageProvider(model: string): 'openai' | 'gemini' | 'xai' {
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

This reference should be used alongside the implementation examples in the next documentation files.
# AI Model Provider Reference

## Complete Model Inventory

This reference contains all working AI models from the comprehensive application testing, including current implementations and legacy configurations.

### OpenAI Models
**Status**: ✅ Currently Active  
**Implementation**: TypeScript (server/ai-service.ts), Python (ai_integrations/llm_handler.py)

```javascript
// Current working models
const openaiModels = {
  // Latest GPT-4 Series
  "gpt-4o": "Primary text model (May 2024)",
  "gpt-4o-mini": "Faster, smaller GPT-4o",
  "gpt-4-turbo": "GPT-4 turbo version",
  "gpt-4": "Standard GPT-4",

  // O-Series (Reasoning)
  "o1": "O1 reasoning model",
  "o1-mini": "Smaller O1 model", 
  "o1-preview": "O1 preview version",
  "o1-pro": "O1 professional version",
  "o3": "Latest O3 model",
  "o3-mini": "Smaller O3 model",
  "o4-mini": "O4 mini model",

  // Legacy
  "gpt-3.5-turbo": "Legacy but still working",

  // Image Generation
  "dall-e-3": "Primary image model",
  "dall-e-2": "Legacy image model",

  // Audio/Speech
  "whisper-1": "Speech-to-text",
  "tts-1": "Text-to-speech",
  "tts-1-hd": "High-quality TTS",

  // Embeddings
  "text-embedding-3-large": "Large embeddings",
  "text-embedding-3-small": "Small embeddings",
  "text-embedding-ada-002": "Legacy embeddings"
};
```

### Google Gemini Models
**Status**: ✅ Currently Active (Primary Image Provider)  
**Implementation**: TypeScript (@google/genai), Python (google.generativeai)

```javascript
const geminiModels = {
  // Gemini 2.5 Series (Latest)
  "gemini-2.5-flash-preview-04-17": "Latest Gemini 2.5",
  "gemini-2.5-pro-preview-03-25": "Gemini 2.5 Pro",

  // Gemini 2.0 Series 
  "gemini-2.0-flash": "Gemini 2.0 Flash",
  "gemini-2.0-flash-preview-image-generation": "Primary image model",
  "gemini-2.0-flash-exp-image-generation": "Experimental image",
  "gemini-2.0-flash-lite": "Lightweight version",

  // Gemini 1.5 Series
  "gemini-1.5-pro": "Gemini 1.5 Pro",
  "gemini-1.5-flash": "Fast Gemini 1.5",
  "gemini-1.5-pro-latest": "Latest Pro version",
  "gemini-1.5-flash-latest": "Latest Flash version",

  // Gemma 3 Series (FREE - Prompt Enhancement)
  "gemma-3-1b-it": "Gemma 3 1B (FREE) - Primary prompt enhancement",
  "gemma-3-4b-it": "Gemma 3 4B (FREE) - Enhanced prompt quality",
  "gemma-3-12b-it": "Gemma 3 12B (FREE) - High-quality enhancement (default)",
  "gemma-3-27b-it": "Gemma 3 27B (FREE) - Premium prompt enhancement",
  "gemma-3n-e4b-it": "Gemma 3N E4B (FREE) - Specialized variant",

  // Legacy
  "gemini-pro-vision": "Vision capabilities",
  "gemini-pro": "Legacy Gemini Pro",
  "gemini-ultra": "Ultra model"
};
```

### X.AI (Grok) Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with X.AI endpoint

```javascript
const xaiModels = {
  // Grok 3 Series (Latest)
  "grok-3-beta": "Latest Grok 3",
  "grok-3-mini": "Smaller Grok 3",
  "grok-3-fast-beta": "Fast Grok 3",
  "grok-3-mini-fast-beta": "Mini fast version",

  // Grok 2 Series
  "grok-2-1212": "Grok 2 text model",
  "grok-2-vision-1212": "Grok 2 vision",
  "grok-2-image-1212": "Grok 2 image generation",
  "grok-2-image-latest": "Latest image model",

  // Legacy
  "grok-beta": "Legacy Grok beta",
  "grok-vision-beta": "Legacy vision beta"
};
```

### Anthropic Claude Models
**Status**: ✅ Currently Active  
**Implementation**: Direct HTTP requests

```javascript
const anthropicModels = {
  "claude-3-5-sonnet-20241022": "Latest Claude 3.5 (Oct 2024)",
  "claude-3-opus-20240229": "Most capable Claude 3",
  "claude-3-sonnet-20240229": "Balanced Claude 3",
  "claude-3-haiku-20240307": "Fastest Claude 3",
  "claude-2": "Legacy Claude 2",
  "claude-instant-1": "Fast legacy model"
};
```

### DeepSeek Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with DeepSeek endpoint

```javascript
const deepseekModels = {
  "deepseek-chat": "General purpose",
  "deepseek-reasoner": "Reasoning specialized",
  "deepseek-coder": "Code specialized (recommended)"
};
```

### Nvidia Nemotron Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with Nvidia endpoint

```javascript
const nvidiaModels = {
  "nemotron-4-340b": "Ultra large 340B model",
  "nemotron-4-midi": "Mid-sized model",
  "nemotron-4-mini": "Smaller, faster model",
  "nemotron-3-8b": "8B parameter model"
};
```

### Perplexity Models
**Status**: ✅ Currently Active  
**Implementation**: OpenAI client with Perplexity endpoint

```javascript
const perplexityModels = {
  "llama-3.1-sonar-large-128k-online": "Large with web search",
  "llama-3.1-sonar-small-128k-online": "Small with web search",
  "sonar-large-chat": "Large without search",
  "sonar-small-chat": "Small without search",
  "mixtral-8x7b-instruct": "Mixtral 8x7B",
  "mistral-7b-instruct": "Mistral 7B"
};
```

### NVIDIA NIM Models
**Status**: ✅ Working - Via X.AI API Gateway
**API Base**: `https://integrate.api.nvidia.com/v1`
**Models Available**:
- `nvidia/llama-3.1-nemotron-70b-instruct` - ✅ Working
- `meta/llama-3.1-8b-instruct` - ✅ Working  
- `meta/llama-3.1-70b-instruct` - ✅ Working
- `microsoft/phi-3-mini-128k-instruct` - ✅ Working
- `google/gemma-2-9b-it` - ✅ Working for text tasks
- `google/gemma-2-27b-it` - ✅ Working for text tasks

### Google Gemma-3 Models (via NVIDIA)
**Status**: ✅ Working - Specialized for prompt enhancement
**API Base**: `https://integrate.api.nvidia.com/v1`
**Models Available**:
- `google/gemma-3-8b-it` - ✅ Working - **Used for prompt enhancement**
- `google/gemma-3-2b-it` - ✅ Working - Lightweight option
- `google/gemma-3-27b-it` - ✅ Working - High-performance option

**Special Use Case**: These Gemma-3 models are specifically configured in our enhance prompt functions for improving user prompts before sending to image generation models.

## API Endpoint Configuration

### Environment Variables Required
```bash
# Primary providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
DEEPSEEK_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
PERPLEXITY_API_KEY=pplx-...
```

### Provider Endpoints
```javascript
const endpoints = {
  openai: "https://api.openai.com/v1",
  google: "https://generativelanguage.googleapis.com",
  anthropic: "https://api.anthropic.com",
  xai: "https://api.x.ai/v1",
  deepseek: "https://api.deepseek.com",
  nvidia: "https://integrate.api.nvidia.com/v1",
  perplexity: "https://api.perplexity.ai"
};
```

## Working Model Status Matrix

| Provider | Text Generation | Image Generation | Prompt Enhancement | Image Editing | Status |
|----------|----------------|------------------|-------------------|---------------|---------|
| OpenAI | ✅ gpt-4o | ✅ dall-e-3 | ✅ gpt-4o-mini | ❌ | Active |
| Google | ✅ gemini-2.5-flash | ✅ gemini-2.0-flash-preview | ✅ **gemma-3-12b-it (FREE)** | ✅ | Primary |
| X.AI | ✅ grok-3-beta | ✅ grok-2-image-latest | ✅ grok-2-1212 | ✅ (via Gemini) | Active |
| Anthropic | ✅ claude-3-5-sonnet | ❌ | ✅ claude-3-5-sonnet | ❌ | Active |
| DeepSeek | ✅ deepseek-coder | ❌ | ✅ deepseek-chat | ❌ | Active |
| Nvidia | ✅ nemotron-4-340b | ❌ | ❌ | ❌ | Active |
| Perplexity | ✅ llama-3.1-sonar | ❌ | ❌ | Active |

## Deprecated/Removed Models
```javascript
// These models were removed or are no longer working
const deprecatedModels = {
  "gemma-3-1b-it": "Not implemented in LLMModelMapper",
  "gemma-7b": "Removed from working implementation", 
  "gemma-2b": "Removed from working implementation",
  "gpt-4.1": "Listed in llm_handler.py but not verified working",
  "gpt-4.1-mini": "Listed in llm_handler.py but not verified working"
};
```

## Integration Notes

### Current Primary Configuration
- **Text Generation**: OpenAI gpt-4o (default), user-configurable
- **Image Generation**: Google Gemini 2.0 Flash Preview (primary)
- **Image Editing**: Google Gemini (all editing routes through Gemini)
- **Prompt Enhancement**: **Gemma-3-12b-it (FREE)** as default, user-configurable

### Free Model Advantages
- **Gemma-3 Series**: Completely FREE models via Google API
- **No API costs**: Perfect for prompt enhancement without usage charges
- **High quality**: Gemma-3-12b-it provides excellent prompt enhancement
- **Multiple sizes**: Choose based on speed vs quality preferences
```typescript
// From server/ai-service.ts
function getImageProvider(model: string): 'openai' | 'gemini' | 'xai' {
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

This reference should be used alongside the implementation examples in the next documentation files.