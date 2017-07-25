#!/usr/bin/env bash

git pull
./gradlew tag -Prelease
./gradlew publish
./gradlew tag -PbumpComponent=patch
git push