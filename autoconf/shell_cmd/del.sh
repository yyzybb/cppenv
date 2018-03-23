#!/bin/bash

grep "$1" * -rn | cut -d: -f1 | xargs sed -i "/${1}/d"
