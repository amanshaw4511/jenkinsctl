# jenkinsctl [![PyPI version](https://badge.fury.io/py/jenkinsctl.svg)](https://badge.fury.io/py/jenkinsctl) [![Downloads](https://static.pepy.tech/badge/jenkinsctl/week)](https://pepy.tech/project/jenkinsctl)
Build Jenkins jobs effortlessly using a single command. 🚀

## Installation 📦

```sh
pip install jenkinsctl
```

## Jenkins Configuration 🛠️
Before using jenkinsctl, configure your Jenkins server details in your shell profile.
Add these lines in your ~/.bashrc or ~/.zshrc file:
```sh
export JENKINS_SERVER_URL=http://localhost:8080
export JENKINS_USERNAME=amanshaw4511
export JENKINS_API_KEY=21df49caf41726094323b803a6de363eae
```
Adjust the values to match your Jenkins server's URL, your username, and the corresponding API key. This configuration is essential for jenkinsctl to interact with Jenkins and execute tasks efficiently.

How to Get the API Token: https://www.baeldung.com/ops/jenkins-api-token
## Usage 🤖
```sh
$ jenkinsctl --help
usage: jenkinsctl [-h] {build,config} ...

options:
  -h, --help      show this help message and exit

Subcommand:
  {build,config}
    build         run new build
    config        get config of a build
```

### Run a Jenkins Job
```sh
$ jenkinsctl build --help
usage: jenkinsctl build [-h] [-f FILE] [-v] [-s SUPPRESS_LOGS] [--param PARAM]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Yaml configuration file
  -v, --verbose
  -s SUPPRESS_LOGS, --suppress-logs SUPPRESS_LOGS
  --param PARAM
```

### Get Config of a Jenkin Build in YAML Format
```sh
$ jenkinsctl config --help
usage: jenkinsctl config [-h] job_name build_no

positional arguments:
  job_name
  build_no

options:
  -h, --help  show this help message and exit
```

## Examples 🎭
### Runing a Jenkins Job
Create a YAML configuration file, let's say `my_job.yaml`, with job parameters like this:
```yaml
job: my_job
params:
    param1: some value
    param2: 10
    param3: true
```
Initiate the job build using the following command:
```sh
jenkinsctl build -f my_job.yaml
```
This command executes the job based on the specified YAML configuration.

### Overriding Specific Parameter from Configuration
```sh
jenkinsctl build -f my_job.yaml --param param2=11 --param param3=false
```
This command will override the value of `param2` and `param3` from original configuration file `my_job.yaml`, passing an effective configuration as follows to run jenkin job :
```yaml
job: my_job
params:
    param1: some value
    param2: 11
    param3: false
```
.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/shtab.svg?label=pypi%20downloads&logo=PyPI&logoColor=white
   :target: https://pepy.tech/project/shtab
   :alt: Downloads

### Generating Config from Existing Builds
Capture and reproduce configurations from previous Jenkins builds.
To generate a YAML configuration file from a specific build (e.g. 2nd build) of a job (e.g., `my_job`), use the following command:
```sh
jenkinsctl config my_job 2 > my_job.yaml
```
