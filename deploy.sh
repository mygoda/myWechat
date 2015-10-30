#!/usr/bin/env bash

git pull

supervisorctl update
supervisorctl restart my