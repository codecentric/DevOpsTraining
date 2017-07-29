# Exercise 007 - Blue/Green deployments

In this exercise support for blue/green deployments is added. The support in concourse itself is limited for such 
operations but with the proper scripts and supporting application this behavior can be available.

In the platform VM [Traefik](https://traefik.io/) in combination with docker is used. By setting lables on the 
container the routing is handled.