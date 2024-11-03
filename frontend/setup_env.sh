#!/bin/bash

# Environment Variable that will be configurate in pipeline
SONAR_TOKEN=$1

# Verifying whether .env file already exist
if [ -f .env ]; then
  echo ".env file already exists. Skipping creation."
  echo "::set-output name=env_created::false"
else
  # Creating .env file with SONAR_TOKEN var
  echo "SONAR_TOKEN=$SONAR_TOKEN" > .env

  echo ".env file has been created."
  echo "::set-output name=env_created::true"
fi
