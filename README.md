# popupchecker

This tool makes screenshots of pages.

# Usage
To use in Windows: change os chromedriver variable in settings to "" and ensure that chromedriver.exe in the project's folder.
To use in Linux: make sure that os chromedriver variable in settings is set to "/usr/local/bin/chromedriver"

# Docker commands

To build it: 
  ```
  docker build --tag=tvmpopups .
  ```
To run it:
  ```
  docker run -p 8000:8000 tvmpopups
  ```
To stop it:
  ```
  docker container ls
  docker container stop {container id}
  ```
## To push it to Docker Hub and run it from there
To tag it (needs for push into Docker Hub):
  ```
  docker tag tvmpopups {docker hub username}/tvmpopups:{version name, e.g.: v1}
  ```
To push it:
  ```
  docker push {docker hub username}/tvmpopups:{version name from previous command}
  ```
To run it:
  ```
  docker run -p 8000:8000 {docker hub username}/tvmpopups:{version name from previous commands}
  ```
