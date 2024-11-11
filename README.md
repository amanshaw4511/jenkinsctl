![jenkinsctl](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/226px-Jenkins_logo.svg.png?20120629215426)
# jenkinsctl [![PyPI version](https://badge.fury.io/py/jenkinsctl.svg?)](https://badge.fury.io/py/jenkinsctl) [![Downloads](https://static.pepy.tech/badge/jenkinsctl/week?)](https://pepy.tech/project/jenkinsctl) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
Build Jenkins jobs effortlessly using a single command. 🚀
`jenkinsctl` is a command-line tool built to make Jenkins management fast and efficient, putting powerful job control at your fingertips. Whether you're listing builds, fetching logs, or triggering parameterized jobs, `jenkinsctl` simplifies your CI/CD workflow.

## 🧩 Why jenkinsctl?

Working through Jenkins' UI for routine tasks can be tedious. `jenkinsctl` lets you skip the web interface, saving time and bringing Jenkins control directly into your terminal.

### Key Features

- **Quick Build Listings**: View recent builds for any job.
- **Instant Log Access**: Fetch build logs effortlessly.
- **JSON & YAML API Data**: Retrieve job configurations and build data in JSON or YAML.
- **Easy Rebuilds**: Re-run jobs without reopening Jenkins.
- **Parameterized Builds**: Customize builds with dynamic parameters.
- **Folder Job Listings**: Organize and access jobs in specific folders.
- **Autocompletion**: Enhance the CLI experience with shell autocompletion for bash, zsh, or fish.

---

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

### Generating Config from Existing Builds
Capture and reproduce configurations from previous Jenkins builds.
To generate a YAML configuration file from a specific build (e.g. 2nd build) of a job (e.g., `my_job`), use the following command:
```sh
jenkinsctl config my_job 2 > my_job.yaml
```
