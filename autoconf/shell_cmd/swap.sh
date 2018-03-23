#!/bin/bash

grep "$1" * -rn | cut -d: -f1 | xargs sed -i "s/${1}/${2}/g"
