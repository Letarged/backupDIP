# Dipscan - Tool For Automted Penetration Testing

 
> **Thanks:** I am grateful you chose Dipscan tool. Please note that there are some validations against incorrect user inputs and malformated user-defined add-ons, but it is far from being complete. Just "Sem-tam"


## Installation steps

In order to install the tool it is enough to download the repository and run `setup.py` as shown here:
```bash
git clone https://github.com/Letarged/backupDIP.git
cd backupDIP
sudo ./setup.py install
```
It will take several minutes (5-10mins).Before starting the installation, there are several dependencies that need to be satisfied. Some of these dependencies are not covered by the installation process. If any dependencies are missing, please refer to the following table for guidance on how to resolve the issue:
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
# in repo, by default, the config has all the modules switched on
sudo dipscan SINGLE hackthissite.org
```

## Modules
The whole tool is composed from several modules. It is designed to be easy to add another modules according to the user's specific needs. In general, each module consists of:
1. Record in `dipmodules.py`
2. A python file containing a function for the command creation
3. New entry in the config-run file

## Adding a user-defined modules

Since one the the primal features of the tool is its extensibility, here is a short tutorial how to extend the tool's functionality by writing user module.
#### Steps for creating a module based on a linux-command-line tool 
Install the tool on the PC. It is recommended to make sure the chosen tool provides some form of standardized output (ex. XML, JSON,...) which can be easily parsed later. If not, the parsing process might become quite challenging. 

Create a Dockerfile with the tool's installation command and correct entrypoint. (Feel free to copy and modify one of the existing Dockerfiles).` 

Example of a `Dockerfile`:
```docker
FROM  ubuntu

#COPY ./app /app

#WORKDIR /app

RUN  apt  update  &&  apt  install  -y  \
whatweb

ENTRYPOINT  [  "whatweb"  ]
CMD  ["--help"]
```
Create an image out of this Dockerfile. The following command will work if it's run in the location with the Dockerfile:

```
sudo docker build -t imagename .
```
Add a record into `dipmodules.py` . Just like other, built-it, modules, also the user-defined must be connected to the tool. In order to correctly map the new module, append a new pair "key - value", to `dipmodules.py` where `key` can be considered as ***the name of the new module*** (this name will be important later), while  `value` is a dictionary containing several "key - value"pairs. The minimum 4 keys which are mandatory are: `'image'`, `'service'`, `'command'` and `'params'`, More details can be found in the previous section of this text. To get the default location of  `dipmodules.py` file, run `sudo dipscan CONF`. Here is an example of such a record in `dipmodules.py`:

```python
'Whatweb' : {
	'image' : 'dwhatweb:v1',
	'service' : 'https',
	'params' : '-a1',
	'command' : 'src.cores.whatweb.whatweb_core.craftWhatwebCommand',
	'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'
	}
```
Write the functions which were specified in the previous step (`command` and `parser`). In the above example, it is `craftWhatwebCommand()` function in a python file called `whatweb_core.py`, which is located in `src/cores/whatweb`. Your functions can be in any file (and even specified with the absolute path), it's just necessary to point to them in the record in `dipmodules.py`. 

Function, towards which is being pointed using `'command'` , takes 3 arguments: 
* **`target`**
* **`param`**
* **`port`**

Returns a string (a command), which is equivalent to the text we normally write in command line after the name of the tool. This includes specification regarding the from of the output of the tool (ex. --xml=-). This function is also responsible for putting the `target` into the correct form, which possibly means converting an IP into an URI, adding "https://" prefix, adding ":443" suffix, etc.

Function, towards which is being pointed using `'parser'` , takes 1 argument:  
* **`output`** - raw output of the tool
Return the (optionally colored) string which is the final form of output being printed by Dipscan.


Returns a string, which is equivalent to the text we normally write in command line after the name of the tool.


Next step is adding an entry into `run.cfg`  like this:

```ruby
[Whatweb]
switched_on = 1
```
The name in [*brackets*] must be the same as ***the name of the new module*** specified in `dipmodules.py` (which we did earlier in this text).


#### Steps for creating a module based on a python function
It is also possible to add a module which is defined just by a python code, without its docker image. In this case..

## Notes
There is a default `dipmodules.py` file along with a default `run.cfg` configuration file in the repository. Once Dipscan is downloaded and installed, they are copied into the system's default location for configuration files (which in my case happened to be `/root/.config/dipconf/`). Note that this info can be printed out using `sudo dipscan CONF` command, since the system's default location may vary from system to system. . And that's exactly the location, which metadata for the tool's run is loaded from. Therefore, the instances of default files which were downloaded from git remain untouched during the rest of the time of this world. Every time you execute this tool, it looks for `dipmodules.py` and `run.cfg` in the system’s default location for configuration files (unless overwritten using `-r` or `-m` option)(see `--help` for more info).