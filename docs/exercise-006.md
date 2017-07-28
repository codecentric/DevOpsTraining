# Exercise 006 - Run on blue

Now it time to run the software. In this case the underlaying docker layer is used to run the software. This done by 
accessing the docker API through for this training build docker interface. This will create a running docker container 
with the application in it.

## Setup the run task

To create the run task follow these steps:

- Extend the **pipeline.yml** file with a new job called **run**. This job will be triggered after the job **deploy** 
has been finished. 
```yaml
- name: run
  plan:
  - get: sources # Download the sources
    trigger: true
    passed: [deploy] # Trigger after job test has passed
  - task: run the application in the blue environment
    file: sources/CI/task-run.yml
``` 
- Create a new file **task-run.yml** in the **CI** directory. This task will create (and replace) a the application in 
the blue environment. Add the following content to the **task-run.yml** file:
```yaml
platform: linux

image_resource:
  type: docker-image
  source: {repository: openjdk, tag: 8}

run:
  path: ./gradlew # Command to execute
  args: ["build"]
  dir: sources/application # Location to execute, note the 'sources' as directory prefix

run: # Gradle release + version bumping
  path: sh
  args:
  - -exc
  - |
    VERSION=$(curl -X GET http://consul.service.consul:8500/v1/kv/version?raw=true)
    ENVIRONMENT="blue"
    DOWNLOAD_URL="http://nexus.service.consul:8081/nexus/content/repositories/releases/nl/codecentric/devops/training/devops-training-application/$VERSION/devops-training-application-$VERSION.jar"
    curl "http://run-on-docker.service.consul:8000/?application=$DOWNLOAD_URL&environment=$ENVIRONMENT&version=$VERSION"
    curl -X PUT -d "$ENVIRONMENT" http://consul.service.consul:8500/v1/kv/environment
``` 
- Commit the changes and push them
- After a few moments a new build is triggered
- Update the pipeline with ```$ fly -t lite set-pipeline -p devops-training -c pipeline.yml --load-vars-from secrets.yml```
- After a successful run of the pipeline the blue environment will be available.
