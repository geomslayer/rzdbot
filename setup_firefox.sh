#!/bin/bash
set -e

if [ -n "${RESOLUTION}" ]; then
    OPTS="-screen 0 ${RESOLUTION}"
fi

Xvfb :1 ${OPTS} &
export DISPLAY=:1

$@