# Dipscan - Tool For Automted Penetration Testing

 
> **Thanks:** I am grateful you chose Dipscan tool.


## Installation steps

In order to install the tool it is enough to download the repository and run `setup.py` as shown here:
```bash
git clone https://github.com/Letarged/backupDIP.git
cd backupDIP
sudo ./setup.py install
```
Several dependencies are required even before starting the installation and some of them are not covered in the installation process, the following table provides help on how to solve if anything is missing:
|              Tool / Library  |How to solve if missing                          |
|----------------|-------------------------------|
|git|`sudo apt install git -y`            |
|python3          |`sudo apt install python3 -y`            |
|pip          |`sudo apt install python3-pip -y`|
|python3/appdirs          |`sudo pip install appdirs`|
|python3/setuptools         |`sudo pip install setuptools`|
|python3/termcolor         |`sudo pip install termcolor`|
|python3/docker         |`sudo pip install docker`|

Since `dipscan` uses docker images, it must be run as root. The tool can be run by the following command:
```bash
# print help
sudo dipscan --help

# run a simple scan with the default settings
sudo dipscan SINGLE hackthissite.org
```
