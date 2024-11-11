![jenkinsctl](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/226px-Jenkins_logo.svg.png?20120629215426)
# jenkinsctl [![PyPI version](https://badge.fury.io/py/jenkinsctl.svg?)](https://badge.fury.io/py/jenkinsctl) [![Downloads](https://static.pepy.tech/badge/jenkinsctl/week?)](https://pepy.tech/project/jenkinsctl) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# jenkinsctl – Jenkins Control Right from Your Terminal 🚀

`jenkinsctl` is a CLI tool that puts Jenkins management right in your terminal. It simplifies tasks like listing builds, fetching logs, and triggering parameterized jobs—no more web UI hassle!

## Why jenkinsctl? 🔥

Jenkins workflows can be tedious through the web UI. `jenkinsctl` keeps your hands on the keyboard, streamlining Jenkins management directly from your terminal, making it perfect for quick job control, scripting, and automation.

---

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
pip3 install jenkinsctl
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

Reload your shell profile:
```sh
exec $SHELL
```

## Commands & Options 🤖
All `jenkinsctl` commands are designed to be terminal-friendly with structured flags and arguments.

### `list`
List recent builds of a Jenkins job.
```sh
jenkinsctl list <job_name> [-n <number_of_builds>]
```
| Option         | Description                                    |
|----------------|------------------------------------------------|
| `job_name`     | Name of the Jenkins job                        |
| `-n, --number` | Number of builds to list (default: 5)          |

### `logs`
View logs of a specific build.
```sh
jenkinsctl logs <job_name> [build_no]
```
| Option      | Description                                       |
|-------------|---------------------------------------------------|
| `job_name`  | Name of the Jenkins job                           |
| `build_no`  | Build number (optional, defaults to last build)   |

### `json`
Get JSON API data for a build.
```sh
jenkinsctl json <job_name> [build_no]
```
### `config`
Get build configuration in YAML format.
```sh
jenkinsctl config <job_name> [build_no]
```

### `rebuild`
Trigger a rebuild of a specific job.
```sh
jenkinsctl rebuild <job_name> [build_no]
```

### `build`
Start a new build using YAML configuration with optional parameters.
```sh
jenkinsctl build -f <config_file> [--param key=value]
```
| Option         | Description                                     |
|----------------|-------------------------------------------------|
| `-f, --file`   | YAML configuration file for the Jenkins job     |
| `--param`      | Key-value pairs to override config parameters   |

### `enable-completion`
Enable shell autocompletion for streamlined CLI use.
```sh
jenkinsctl enable-completion [shell]
```
| Argument | Description                                           |
|----------|-------------------------------------------------------|
| `shell`  | Optional: specify shell (`bash`, `zsh`, or `fish`)    |

### `jobs`
List all jobs in a specified Jenkins folder.
```sh
jenkinsctl jobs [folder_name]
```
| Option       | Description                                   |
|--------------|-----------------------------------------------|
| `folder_name`| Folder path for jobs (optional)               |


## Quick Examples 🎭

1. **List Recent Builds**: Show the last 10 builds for a job.
    ```
    jenkinsctl list my-awesome-job -n 10
    ```

2. **Get Logs for a Build**: View logs for a specific build.
    ```
    jenkinsctl logs my-awesome-job 42
    ```

3. **Start a Build with Parameters**: Launch a build with custom parameters.
    ```
    jenkinsctl build -f path/to/config.yaml --param version=1.2.3
    ```

---

## Contributing 🤝

Contributions are welcome! If you want to contribute, fork the repo, make your changes, and submit a pull request. Found an issue? Open an issue in the repo!

---

