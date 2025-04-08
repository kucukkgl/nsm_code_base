#!/bin/bash

echo "🔹 Step 1: Installing dependencies..."
pip3 install selenium mitmproxy || { echo "❌ Failed to install dependencies"; exit 1; }

echo "🔹 Step 2: Downloading Geckodriver..."
curl -L -o geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-macos.tar.gz

if [ ! -f "geckodriver.tar.gz" ]; then
    echo "❌ Failed to download Geckodriver"; exit 1;
fi

echo "🔹 Step 3: Installing Geckodriver..."
tar -xvzf geckodriver.tar.gz
sudo mv geckodriver /usr/local/bin/
chmod +x /usr/local/bin/geckodriver
rm geckodriver.tar.gz

echo "🔹 Step 4: Verifying installation..."
if geckodriver --version; then
    echo "✅ Geckodriver installed successfully!"
else
    echo "❌ Geckodriver installation failed"; exit 1;
fi

echo "✅ Setup complete. You can now run the Python script!"
