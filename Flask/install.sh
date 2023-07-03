# SeleniumBase Debian Linux Dependency Installation
# (Installs all required dependencies on Linux)
# Initial version copied from:
# https://github.com/seleniumbase/SeleniumBase/blob/3f60c2e0fd78807528661aff36120700d4ff1ed6/integrations/linux/Linuxfile.sh

# Make sure this script is only run on Linux
value="$(uname)"
if [ "$value" = "Linux" ]
then
  echo "Initializing Requirements Setup..."
else
  echo "Not on a Linux machine. Exiting..."
  exit
fi

# Go home
cd ~

# Configure apt-get resources
sh -c "echo \"deb http://packages.linuxmint.com debian import\" >> /etc/apt/sources.list"
sh -c "echo \"deb http://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt all main\" >> /etc/apt/sources.list"

# Update aptitude
apt-get update

# Install core dependencies
apt-get install -y --force-yes unzip
apt-get install -y --force-yes xserver-xorg-core
apt-get install -y --force-yes x11-xkb-utils

# Install Xvfb (headless display system)
apt-get install -y --force-yes xvfb

# Install fonts for web browsers
apt-get install -y --force-yes xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic

# Install Python core dependencies
apt-get update
apt-get install -y --force-yes python-setuptools

# Install Firefox
gpg --keyserver pgp.mit.edu --recv-keys 3EE67F3D0FF405B2
gpg --export 3EE67F3D0FF405B2 > 3EE67F3D0FF405B2.gpg
apt-key add ./3EE67F3D0FF405B2.gpg
rm ./3EE67F3D0FF405B2.gpg
apt-get -qy --no-install-recommends install -y --force-yes firefox
apt-get -qy --no-install-recommends install -y --force-yes $(apt-cache depends firefox | grep Depends | sed "s/.*ends:\ //" | tr '\n' ' ')
wget --no-check-certificate -O firefox-esr.tar.bz2 'https://download.mozilla.org/?product=firefox-esr-latest&os=linux32&lang=en-US'
tar -xjf firefox-esr.tar.bz2 -C /opt/
rm -rf /usr/bin/firefox
ln -s /opt/firefox/firefox /usr/bin/firefox
rm -f /tmp/firefox-esr.tar.bz2
apt-get -f install -y --force-yes firefox

# Install more dependencies
apt-get update
apt-get install -y --force-yes xvfb
apt-get install -y --force-yes build-essential chrpath libssl-dev libxft-dev
apt-get install -y --force-yes libfreetype6 libfreetype6-dev
apt-get install -y --force-yes libfontconfig1 libfontconfig1-dev
apt-get install -y --force-yes python-dev

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get -f install -y --force-yes
dpkg -i google-chrome-stable_current_amd64.deb

# Install Chromedriver
wget -N https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
chmod +x chromedriver
rm -f /usr/local/share/chromedriver
rm -f /usr/local/bin/chromedriver
rm -f /usr/bin/chromedriver
mv -f chromedriver /usr/local/share/chromedriver
ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

#============
# GeckoDriver
#============
GECKODRIVER_VERSION=latest
GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo $(wget -qO- "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([0-9.]+)".*/\1/'); else echo $GECKODRIVER_VERSION; fi)
echo "Using GeckoDriver version: "$GK_VERSION
wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz
rm -rf /opt/geckodriver
tar -C /opt -zxf /tmp/geckodriver.tar.gz
rm /tmp/geckodriver.tar.gz
mv /opt/geckodriver /opt/geckodriver-$GK_VERSION
chmod 755 /opt/geckodriver-$GK_VERSION
ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

# Finalize apt-get dependancies
apt-get -f install -y --force-yes

# Get pip
easy_install pip
dpkg -i google-chrome-stable_current_amd64.deb
google-chrome-stable --version
# get python dependency
wget -O requirements.txt https://raw.githubusercontent.com/garywu/gae-selenium/master/requirements.txt
pip install -r requirements.txt
wget -O demo.py https://raw.githubusercontent.com/garywu/gae-selenium/master/demo.py
chmod +x demo.py
wget -O start_headless.sh https://raw.githubusercontent.com/garywu/gae-selenium/master/start_headless.sh
chmod +x start_headless.sh
