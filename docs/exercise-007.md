# Exercise 007 - Blue/Green deployments

In this exercise support for blue/green deployments is added. The support in concourse itself is limited for such 
operations but with the proper scripts and supporting application this behavior can be available.

In the platform VM [Traefik](https://traefik.io/) in combination with docker is used. By setting lables on the 
container the routing is handled.

The provisioning happens through a specialized Python application. This application will create a docker container with
the version of the application in it. The provisioning application can be found in the GIT repo. 
```$GIT_REPO/run/run-on-docker.py```

For this provisioning other platforms like Ansible, Chef or other frameworks can be used. The platform should provision 
a API to setup an environment.

## Create the blue-green configuration.

To create the run task follow these steps:

- Change the **pipeline.yml** file, in the **run** job replace the **sources/CI/task-run.yml** with 
**sources/CI/task-blue-green.yml** 
```yaml
- name: run
  plan:
  - get: sources # Download the sources
    trigger: true
    passed: [deploy] # Trigger after job test has passed
  - task: run the application in the blue environment
    file: sources/CI/task-blue-green.yml
```
- Create a new file **sources/CI/task-blue-green.yml** and add the following content.
```yaml
platform: linux

image_resource:
  type: docker-image
  source: {repository: openjdk, tag: 8}

run: # Gradle release + version bumping
  path: sh
  args:
  - -exc
  - |
    VERSION=$(curl -X GET http://consul.service.consul:8500/v1/kv/version?raw=true)
    CURRENT_ENVIRONMENT=$(curl -X GET http://consul.service.consul:8500/v1/kv/environment?raw=true)
    DOWNLOAD_URL="http://nexus.service.consul:8081/nexus/content/repositories/releases/nl/codecentric/devops/training/devops-training-application/$VERSION/devops-training-application-$VERSION.jar"
    ENVIRONMENT="blue"
    if [ "$CURRENT_ENVIRONMENT" = "blue" ]; then
      ENVIRONMENT="green"
    elif [ "$CURRENT_ENVIRONMENT" = "green" ]; then
      ENVIRONMENT="blue"
    fi
    curl "http://run-on-docker.service.consul:8000/?application=$DOWNLOAD_URL&environment=$ENVIRONMENT&version=$VERSION"
    curl -X PUT -d "$ENVIRONMENT" http://consul.service.consul:8500/v1/kv/environment
```
- Commit the changes and push them
- After a few moments a new build is triggered
- Update the pipeline with ```$ fly -t lite set-pipeline -p devops-training -c pipeline.yml --load-vars-from secrets.yml```
- After a successful run of the pipeline environment will be available.
- This can be checked with the following command ```$ curl http://localhost:4080/app```
- When a new commit is created and pushed another environment is configured. this could be checked with the previous 
command.
