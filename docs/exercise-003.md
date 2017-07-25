# Exercise 003 - Make pipeline part of source control

Making the pipeline part of the source control, the code becomes the process. Concourse allows for two strategies here, 
every project has its own process or a global process used by a project. In the training the process is tied to the 
application.

## Storing jobs as source code

For storing the build/deploy and run process the process as code is stored in the **CI** directory.

- Create a **CI** directory in the project root
- Add a new file with name **job-build.yml**