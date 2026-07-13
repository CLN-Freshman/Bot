import os
from pathlib import Path

print("=" * 50)
print("🔍 Checking .env file")
print("=" * 50)

# Check current directory
current_dir = Path.cwd()
print(f"📁 Current directory: {current_dir}")

# Check if .env exists
env_file = current_dir / '.env'
print(f"📁 Looking for .env at: {env_file}")

if env_file.exists():
    print("✅ .env file found!")
    
    # Read and display content (mask token)
    with open(env_file, 'r') as f:
        content = f.read()
        for line in content.split('\n'):
            if line.strip() and not line.startswith('#'):
                if line.startswith('BOT_TOKEN='):
                    token = line.replace('BOT_TOKEN=', '').strip()
                    masked = token[:10] + '...' if len(token) > 10 else token
                    print(f"   - BOT_TOKEN={masked}")
                else:
                    print(f"   - {line}")
else:
    print("❌ .env file NOT found!")
    print(f"📁 Please create: {env_file}")

print("=" * 50)