# jenkinsctl
Build jenkins job in simple command and config

## Installation

```sh
pip install jenkinsctl
```

## Configuration
Add these lines in you ~/.bashrc or ~/.zshrc file
```sh
export JENKINS_SERVER_URL=http://localhost:8080
export JENKINS_USERNAME=amanshaw4511
export JENKINS_API_KEY=21df49caf41726094323b803a6de363eae
```

## Usage
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

### Run a jenkins job
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

### Get config of a jenkin build in YAML format
```sh
$ jenkinsctl config --help
usage: jenkinsctl config [-h] job_name build_no

positional arguments:
  job_name
  build_no

options:
  -h, --help  show this help message and exit
```

## Examples
### Runing a jenkins job
Create `my_job.yaml` config file
```yaml
job: my_job
params:
    param1: some value
    param2: 10
    param3: true
```
Run the job
```sh
jenkinsctl build -f my_job.yaml
```

### Running a jenkins job by overriding few params from config
```sh
jenkinsctl build -f my_job.yaml --param param2=10 --param3=false
```

### Generating config from existing build
Generate config from 2nd build of the job `my_job`
```sh
jenkinsctl config my_job 2 > my_job.yaml
```