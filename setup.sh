#!/bin/bash

# Latagan - Quick Setup Script for macOS/Linux

echo "============================================"
echo "Latagan - Online Thrift Store Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "============================================"
echo "Create Admin Account"
echo "============================================"
python manage.py createsuperuser

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the development server, run:"
echo "    python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo ""
