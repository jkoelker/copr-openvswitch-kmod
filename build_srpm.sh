#!/bin/sh

GIT_PATH=$(realpath ./)

mock --dnf --buildsrpm \
     --root fedora-22-x86_64 \
     --scm-enable \
     --scm-option method=git \
     --scm-option package=openvswitch-kmod \
     --scm-option spec=openvswitch-kmod.spec \
     --scm-option write_tar=True \
     --scm-option git_get="git clone ${GIT_PATH} openvswitch-kmod"
