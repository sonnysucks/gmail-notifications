#!/bin/bash
# User data script for Digital Ocean droplet
# This runs when the droplet is created

set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker root

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared-linux-amd64.deb
rm cloudflared-linux-amd64.deb

# Create snapstudio user
useradd -m -s /bin/bash snapstudio
usermod -aG docker snapstudio

# Clone repository
cd /home/snapstudio
sudo -u snapstudio git clone https://github.com/sonnysucks/gmail-notifications.git
cd gmail-notifications

# Create environment file
sudo -u snapstudio cp env.cloudflare.example .env.production

# Generate secret key
SECRET_KEY=$(openssl rand -base64 32)
sudo -u snapstudio sed -i "s/CHANGE_THIS_TO_A_SECURE_RANDOM_STRING_IN_PRODUCTION/$SECRET_KEY/" .env.production

# Update domain
sudo -u snapstudio sed -i "s/yourdomain.com/${domain}/g" .env.production

# Build Docker image
sudo -u snapstudio docker build -f Dockerfile.production -t snapstudio:production .

# Start application
sudo -u snapstudio docker-compose -f docker-compose.cloudflare.yml up -d

# Configure firewall
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 5001/tcp

echo "SnapStudio deployment completed!"

