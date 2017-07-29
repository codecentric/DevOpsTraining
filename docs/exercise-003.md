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
  args: ["build", "-x", "test"]
  dir: sources/application # Location to execute, note the 'sources' as directory prefix
```
- Commit the changes and push them
- After a few moments a new build is triggered
- Update the pipeline with ```$ fly -t lite set-pipeline -p devops-training -c pipeline.yml --load-vars-from secrets.yml```

The reason you first need to commit and push your changes to build-tasks before updating the pipeline, is that Concourse will fetch the task descriptions directly from Git. Without pushing, it doen't know about the task description.
The advantage of course being that your pipeline is really part of the project and the tasks are automatically updated when checking in.
The disadvantage that for structural pipeline changes, you first need to commit and tell Concourse it needs to update the pipeline.

By prefixing a commit with `[ci skip]` you tell Concourse not to trigger the pipeline, which may come in handy for these kind of updates.

Continue to the next exercise to create a test job
