
# AI Integration Dependencies Guide

## Package Manager Commands

### Node.js/TypeScript Projects

#### Core AI Dependencies
```bash
# Primary AI client libraries
npm install openai
npm install @google/genai
npm install @anthropic-ai/sdk  # Optional, direct HTTP used in this app

# Development dependencies
npm install --save-dev @types/node
npm install --save-dev tsx  # For TypeScript execution
```

#### package.json Configuration
```json
{
  "dependencies": {
    "openai": "^4.73.1",
    "@google/genai": "^0.9.0"
  },
  "devDependencies": {
    "@types/node": "^22.10.2",
    "tsx": "^4.19.2"
  },
  "scripts": {
    "test:ai": "tsx tests/quick-model-test.ts",
    "test:gemini": "tsx tests/gemini-working-test.ts",
    "test:grok": "tsx tests/grok-test.ts"
  }
}
```

### Python Projects

#### Core AI Dependencies
```bash
# Primary AI libraries
pip install openai
pip install google-generativeai
pip install anthropic
pip install requests
pip install python-dotenv

# Development dependencies  
pip install pytest
pip install python-decouple
```

#### requirements.txt
```txt
openai>=1.58.1
google-generativeai>=0.8.3
anthropic>=0.40.0
requests>=2.32.3
python-dotenv>=1.0.1
pytest>=8.3.4
python-decouple>=3.8
markupsafe>=3.0.2
pygments>=2.18.0
```

#### Poetry Configuration (pyproject.toml)
```toml
[tool.poetry.dependencies]
python = "^3.9"
openai = "^1.58.1"
google-generativeai = "^0.8.3"
anthropic = "^0.40.0"
requests = "^2.32.3"
python-dotenv = "^1.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.4"
python-decouple = "^3.8"
```

### Rust Projects

#### Cargo.toml Configuration
```toml
[dependencies]
reqwest = { version = "0.12", features = ["json", "rustls-tls"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.0", features = ["full"] }
dotenv = "0.15"
anyhow = "1.0"

[dev-dependencies]
tokio-test = "0.4"
```

### Java Projects

#### Maven (pom.xml)
```xml
<dependencies>
    <!-- HTTP Client (Java 11+) -->
    <dependency>
        <groupId>org.apache.httpcomponents.client5</groupId>
        <artifactId>httpclient5</artifactId>
        <version>5.3</version>
    </dependency>
    
    <!-- JSON Processing -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.17.0</version>
    </dependency>
    
    <!-- Environment Variables -->
    <dependency>
        <groupId>io.github.cdimascio</groupId>
        <artifactId>dotenv-java</artifactId>
        <version>3.0.0</version>
    </dependency>
    
    <!-- Testing -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

#### Gradle (build.gradle)
```gradle
dependencies {
    implementation 'org.apache.httpcomponents.client5:httpclient5:5.3'
    implementation 'com.fasterxml.jackson.core:jackson-databind:2.17.0'
    implementation 'io.github.cdimascio:dotenv-java:3.0.0'
    
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}
```

## Environment Configuration

### .env Template
```bash
# Primary AI API Keys
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-api03-...
XAI_API_KEY=xai-...
DEEPSEEK_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
PERPLEXITY_API_KEY=pplx-...

# Optional: Custom endpoints
OPENAI_ENDPOINT=https://api.openai.com/v1
GOOGLE_ENDPOINT=https://generativelanguage.googleapis.com
ANTHROPIC_ENDPOINT=https://api.anthropic.com
XAI_ENDPOINT=https://api.x.ai/v1
DEEPSEEK_ENDPOINT=https://api.deepseek.com
NVIDIA_ENDPOINT=https://integrate.api.nvidia.com/v1
PERPLEXITY_ENDPOINT=https://api.perplexity.ai

# Development settings
NODE_ENV=development
LOG_LEVEL=debug
```

### Environment Loading Examples

#### TypeScript/Node.js
```typescript
import dotenv from 'dotenv';
dotenv.config();

// Validation helper
function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Environment variable ${key} is required`);
  }
  return value;
}

// Usage
const openaiKey = requireEnv('OPENAI_API_KEY');
const googleKey = requireEnv('GOOGLE_API_KEY');
```

#### Python
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Validation helper
def require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is required")
    return value

# Usage
openai_key = require_env('OPENAI_API_KEY')
google_key = require_env('GOOGLE_API_KEY')
```

#### Rust
```rust
use dotenv::dotenv;
use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();
    
    let openai_key = env::var("OPENAI_API_KEY")
        .expect("OPENAI_API_KEY must be set");
    let google_key = env::var("GOOGLE_API_KEY")
        .expect("GOOGLE_API_KEY must be set");
        
    Ok(())
}
```

#### Java
```java
import io.github.cdimascio.dotenv.Dotenv;

public class Config {
    private static final Dotenv dotenv = Dotenv.load();
    
    public static String getRequiredEnv(String key) {
        String value = dotenv.get(key);
        if (value == null || value.isEmpty()) {
            throw new IllegalStateException("Environment variable " + key + " is required");
        }
        return value;
    }
    
    public static final String OPENAI_API_KEY = getRequiredEnv("OPENAI_API_KEY");
    public static final String GOOGLE_API_KEY = getRequiredEnv("GOOGLE_API_KEY");
}
```

## Version Compatibility Matrix

### OpenAI Library Versions
| Language | Library | Version | Notes |
|----------|---------|---------|--------|
| TypeScript | `openai` | ^4.73.1 | Latest stable, supports all models |
| Python | `openai` | ^1.58.1 | v1.x required for new API format |
| Rust | `reqwest` | ^0.12 | HTTP client, no official SDK |
| Java | HTTP Client | Built-in | Java 11+ built-in client |

### Google AI Library Versions
| Language | Library | Version | Notes |
|----------|---------|---------|--------|
| TypeScript | `@google/genai` | ^0.9.0 | New unified library |
| Python | `google-generativeai` | ^0.8.3 | Official Python SDK |
| Rust | `reqwest` | ^0.12 | HTTP client approach |
| Java | HTTP Client | Built-in | Direct REST API calls |

## Common Installation Issues

### Node.js Issues
```bash
# Clear cache if packages fail to install
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Use specific Node version (18+ recommended)
nvm use 18
npm install
```

### Python Issues
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with specific Python version
python3.9 -m pip install openai google-generativeai

# Use virtual environment (optional)
python -m venv ai_env
source ai_env/bin/activate  # or ai_env\Scripts\activate on Windows
pip install -r requirements.txt
```

### SSL Certificate Issues
```bash
# Python SSL issues
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org requests

# Node.js SSL issues
npm config set strict-ssl false  # Temporary fix
```

## Testing Dependencies

### Quick Test Scripts

#### TypeScript Test
```typescript
// test-ai-connection.ts
import OpenAI from 'openai';

async function testConnections() {
  const providers = [
    { name: 'OpenAI', test: testOpenAI },
    { name: 'Google', test: testGoogle },
    { name: 'XAI', test: testXAI }
  ];
  
  for (const provider of providers) {
    try {
      await provider.test();
      console.log(`✅ ${provider.name}: Connected`);
    } catch (error) {
      console.log(`❌ ${provider.name}: Failed - ${error.message}`);
    }
  }
}

async function testOpenAI() {
  const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  await client.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: 'test' }],
    max_tokens: 5
  });
}

testConnections();
```

#### Python Test
```python
# test_ai_connections.py
import os
from openai import OpenAI
import google.generativeai as genai

def test_openai():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=5
    )
    return "Connected"

def test_google():
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content('test')
    return "Connected"

if __name__ == "__main__":
    tests = [
        ("OpenAI", test_openai),
        ("Google", test_google)
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}: Connected")
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")
```

This dependency guide should be used alongside the model reference and implementation examples for complete AI integration setup.
