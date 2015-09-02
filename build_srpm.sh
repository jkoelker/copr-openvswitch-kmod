#!/bin/sh

SOURCES=$(realpath ./)
SPEC=openvswitch-kmod.spec

spectool -g ${SPEC}

mock --dnf --buildsrpm \
     --spec=${SPEC} \
     --sources=${SOURCES} \
     --root fedora-22-x86_64 \
