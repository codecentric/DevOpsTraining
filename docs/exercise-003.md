# Exercise 003 - Make pipeline part of source control

Making the pipeline part of the source control, the code becomes the process. Concourse allows for two strategies here, 
every project has its own process or a global process used by a project. In the training the process is tied to the 
application.

## Storing jobs as source code

For storing the build/deploy and run process the process as code is stored in the **CI** directory.

- Create a **CI** directory in the project root
- Add a new file with name **task-build.yml**
- Now move the build task from **pipeline.yml** file to the **task-build.yml** file in the **CI** directory. In the 
**pipeline.yml** file reference the task by replacing the **config** section with **file** property.

**pipeline.yml**
```yaml
# Jobs section
jobs:
- name: build
  plan:
  - get: sources
    trigger: true
  - task: build software
    file: sources/CI/task-build.yml
```

**task-build.yml**
```yaml
platform: linux

image_resource:
  type: docker-image
  source: {repository: openjdk, tag: 8-alpine} # Docker container to build in

inputs:
  - name: sources # Use the source resource

run:
  path: ./gradlew # Command to execute
  args: ["build"]
  dir: sources/application # Location to execute, note the 'sources' as directory prefix
```
- Commit the changes and push them
- After a few moments a new build is triggered
- Update the pipeline with ```$ fly -t lite set-pipeline -p devops-training -c pipeline.yml --load-vars-from secrets.yml```

Continue to the next exercise to create a test job