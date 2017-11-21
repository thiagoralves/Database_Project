#!/bin/bash
echo "Mounting Database..."
sshfs -o IdentityFile=/home/thiagoralves/.ssh/AWS_Key.pem ubuntu@18.216.178.208:/home/ubuntu/ /home/thiagoralves/DB_Project/database/
echo "DONE!"