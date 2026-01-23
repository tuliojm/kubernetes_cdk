#!/bin/bash
# Sample script for additional configuration
echo "Running sample configuration script..."
yum update -y
systemctl status kubelet
echo "Sample script completed"