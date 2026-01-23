#!/bin/bash
# Common setup script for all instances
echo "Running common setup..."
yum update -y
systemctl enable --now containerd
echo "Common setup completed"