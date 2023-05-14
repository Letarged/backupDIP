# Dipscan - Tool For Automted Penetration Testing

 
> **Thanks:** I am grateful you chose Dipscan tool. Please note that there are some validations against incorrect user inputs and malformated user-defined add-ons, but it is far from being complete. Just "Sem-tam"


## Installation steps

In order to install the tool it is enough to download the repository and run `setup.py` as shown here:
```bash
git clone https://github.com/Letarged/backupDIP.git
cd backupDIP
sudo ./setup.py install
```
It will take few minutes (5-10mins). Before starting the installation, there are several dependencies that need to be satisfied. Some of these dependencies are not covered by the installation process. If any dependencies are missing, please refer to the following table for guidance on how to resolve the issue:
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
!! CEWL CHANGE !!

## Modules
The whole tool is composed of several modules. It is designed to be easy to add another modules according to the user's specific needs. In general, each module consists of:
1. A record in `dipmodules.py`
2. Few python functions (specifically 1-3)
3. An entry in the config-run file

#### File `dipmodules.py` in details
Starting with the most important piece of the framewrok, `dipmodules.py` is a python file containing all the metadata needed for a successful run of all the modules. It uses a python dictionary called **`modules`**, where each "key-value" pair represents a module. Key is the name of the module, while value is a nested dictionary with all the important information.
```python
modules = {
	'module1' : {
		#<metadata>
	},
	'module2' : {
		#<metadata>
    }
}
```
An example of a full record of a module:
```python
modules = {
	'Whatweb' : {
		'image' : 'dwhatweb:v1',
		'service' : 'https',
		'params' : '-a1',
		'command' : 'src.cores.whatweb.whatweb_core.craftWhatwebCommand',
		'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'
	},
	#etc..
}
```
As you can see, each record contains several keys with their corresponding value. Not all of them are required, but there is some kind of a standard template for a record.

Minimal keys are those, which the framework counts with during its run. If any of the minimal keys is missing, an error will be raised. The minimal keys are:
* **`'image'`** - A docker image which will run its tool. Note that the entrypoint of the specified image must be set to run that tool. A special value which 'image' can be set to is `None`. In that case, no image will be run. It may be useful in some cases when building a module, especially when the functionality of the module depends solely on a python features.
* **`'service'`** - For which service it is designed. If it's desired to run a module on multiple services, it is necessary to create separate module for that. Service cannot be an array.  Ex. `'https`' or `'domain'`
* **`'params'`** - A string specifying the parameters for the tool. This is quite benevolent since the value will be handled only by the user when writing the functions for the module (see below). So it can be omitted (which is "") and written into that functions. 
* **`'command'`** - Path of a python function which creates the command for the docker run. This function can be defined in any python file in any (accessible) folder, however it is good idea to keep some good practice here. Anyway, the framework will decode the path and run the specified function. Three arguments will be passed:
	1. *type:string* - target address
	2. *type:int* - port
	3. *type:string* - 'params' value from the corresponding module record (untouched by the framework)
	* *return:string* - command which will be supplied to the docker container for its run, which would be equivalent to 
	``` docker run img <returned_string>```

	There are two ways of defining the path of the function, first of which being the "dot" notation, as shown in the example above. It counts with the relative paths so it is expected to be used only with pre-built modules. When defining a user's module, I cannot see a reason why it would be a good idea to use a notation other than this one:
	 `/absolute/path/to/folder/pythonfile.foo ` - Meaning there is a python file `/absolute/path/to/folder/pythonfile.py` containing a definition of `foo()`
* **`'parser'`** - Path of a python function which processes the output of the docker image. The guidelines for specifing this key is the same as above. It takes 1 argument:
	* *type: <something_like_docker_output_idk>* - raw output from docker; in order to get text representation of the output, first action must be the following:
		```python
		data = ""
		for  line  in  output.logs(stream=True):
			data += line.decode("utf-8")
		```
	* *return:string* - a string which will be printed out as a final result of the module (including the extraction of the desired info and formatting, perhaps using termcolor)


There are two more keys, which are recognized by the framework, providing the user with flexibility in creating new modules:
* **`'additional'`** - Path of a python function according to rules described above. This function provides a way for the user to perform any actions which wouldn't be otherwise possible due to strict rules of the framework. It takes 6 arguments, returns nothing:
	1.	*type:string* - command which was created in the function specified in 'command', so the funtion for creating the command can simply return an empty string if it's not needed here (and the execution of the docker image is suppressed by `'image' : None` or by ``'_abort_regular_run'`` (see below)
	2.	*type:string* - target
	3.	*type:port* - port
	4.	*type:dict* - the module with all the "key-vale" pairs
	5.	*type:function* - for printing to stdout and/or to a file, according to `-q` and `-o` options. It takes two parameters, first of which being the 6th argument (see 1 line below). The second argument is a text, which you wish to print as a result of your module. Logically, it can be called multiple times.
	6.	*type:dict* - first argument for the function (see 1 line above) (by the way it contains the info if the `--quiet` option was specified and if `--outputfile OUTPUTFILE` was specified)
		  
* **`'_abort_regular_run'`** - If present, the execution of the docker image won't take place. The value doesn't matter since it is not evaluated whatsoever.

You can add any number of other keys if you find it useful (and use it through the 4th argument of the "additional" function. It won't cause any conflicts.

#### An entry in `run.cfg`   file
Looks like this:
```ruby
[Cewl]
switched_on = 1

[Dnsrecon]
switched_on = 0

[Dnsrecon_reverse]
switched_on = 1
```
If switched on, the module will be run. Can be modified according to the user's needs. Each entry contains the name of the module which must be matching with the name in `dipmodules.py`. Otherwise it won't be possible to pair it.

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
It is also possible to add a module which is defined just by a python code, without a docker image. All the functionality can be covered in "additional" function.. pretty sure it's clear without further description.. I need a rest. 

## Notes
There is a default `dipmodules.py` file along with a default `run.cfg` configuration file in the repository. Once Dipscan is downloaded and installed, they are copied into the system's default location for configuration files (which in my case happened to be `/root/.config/dipconf/`). Note that this info can be printed out using `sudo dipscan CONF` command, since the system's default location may vary from system to system. . And that's exactly the location, which metadata for the tool's run is loaded from. Therefore, the instances of default files which were downloaded from git remain untouched during the rest of the time of this world. Every time you execute this tool, it looks for `dipmodules.py` and `run.cfg` in the system’s default location for configuration files (unless overwritten using `-r` or `-m` option)(see `--help` for more info).

## Common Errors 
- When adding a record to **`modules`** in `dipmodules.py`, triple check if everything is spelled correctly and paths in `'command'`,  `'parser'` and  `'additional'` are correct (you didn't left one one folder in the specified path)
- When using a user-generated docker image, make sure it was generated from correctly written `Dockerfile`, meaning there is a command for the installation of your chosen tool and that the entry point is set correctly as well.