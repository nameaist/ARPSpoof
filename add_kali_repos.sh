#!/bin/bash
echo"      __ _                      ___                 _            _ "
echo"     / /(_)_ __  _   ___  __   / __\__ _ _ __ _ __ (_)_   ____ _| |"
echo"    / / | | '_ \| | | \ \/ /  / /  / _` | '__| '_ \| \ \ / / _` | |"
echo"   / /__| | | | | |_| |>  <  / /__| (_| | |  | | | | |\ V / (_| | |"
echo"   \____/_|_| |_|\__,_/_/\_\ \____/\__,_|_|  |_| |_|_| \_/ \__,_|_|"
echo"                                                                   "
echo "                  Welcome To Linux Carnival                       "
echo "                    code. connect. conquer                        "

set -x  # Enable command echoing

# Update repositories
echo "Running: sudo apt update"
sudo apt update

# Upgrade packages
echo "Running: sudo apt upgrade"
sudo apt upgrade
echo "Running: sudo apt dist-upgrade"
sudo apt dist-upgrade

# Install required packages
echo "Running: sudo apt install curl wget gnupg git"
sudo apt install curl wget gnupg git

# Add Kali Linux repository key
echo "Running: wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add"
wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add

# Add Kali Linux repository to sources list
echo "Running: sudo sh -c \"echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list.d/kali.list\""
sudo sh -c "echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list.d/kali.list"

# Set package preferences for Kali Linux
echo "Running: sudo sh -c \"echo 'Package: *' > /etc/apt/preferences.d/kali.pref; echo 'Pin: release a=kali-rolling' >> /etc/apt/preferences.d/kali.pref; echo 'Pin-Priority: 50' >> /etc/apt/preferences.d/kali.pref\""
sudo sh -c "echo 'Package: *' > /etc/apt/preferences.d/kali.pref; echo 'Pin: release a=kali-rolling' >> /etc/apt/preferences.d/kali.pref; echo 'Pin-Priority: 50' >> /etc/apt/preferences.d/kali.pref"

# Download and install Kali Linux archive keyring
echo "Running: wget http://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb"
wget http://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb
echo "Running: sudo dpkg -i kali-archive-keyring_2022.1_all.deb"
sudo dpkg -i kali-archive-keyring_2022.1_all.deb
echo "Running: rm kali-archive-keyring_2022.1_all.deb"
rm kali-archive-keyring_2022.1_all.deb

# Update repositories again
echo "Running: sudo apt update"
sudo apt update
echo "Running: sudo apt update --fix-missing"
sudo apt update --fix-missing

# Fix any broken dependencies
echo "Running: sudo apt install -f"
sudo apt install -f
echo "Running: sudo apt --fix-broken install"
sudo apt --fix-broken install

# Upgrade packages
echo "Running: sudo apt upgrade"
sudo apt upgrade

set +x  # Disable command echoing
