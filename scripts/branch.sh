#!/bin/bash

RUN=start

function branches() {
    declare -a arr=("main" "release/pre" "release/qa" "develop")

    for i in "${arr[@]}"
    do
      echo "*********************"
      echo "The branch is: $i"
      echo "*********************"
      git branch "$i"
      git checkout "$i"
      git push --set-upstream origin "$i"
      echo "*********************"
    done
}

function start() {
    branches
}

$RUN
