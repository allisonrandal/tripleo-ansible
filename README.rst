TripleO on Ansible
==================

At heart, TripleO is an architecture and an API, using OpenStack
components within the deployment process for OpenStack clouds.
Currently, TripleO is also a monolithic implementation, mostly written
in Bash shell scripts. Although this implementation was originally
only intended as a spin-up for development and testing environments
(hence the name "devtest"), because it is the only fully functional
implementation of TripleO, people have started to view it as the core
definition of TripleO as a project. The monolithic implementation is
seen as an "all or nothing" competitor to OpenStack deployment methods
in Chef/Puppet/Salt/Ansible/Juju/etc, when in fact TripleO was always
intended to have pluggable backends written in any tooling.

This project is an experimental proof-of-concept in delivering the
TripleO architecture over an alternate backend.

Getting started
---------------

For testing purposes this first approximation is designed to run
within an existing public OpenStack cloud. Spin up an initial
instance, and install required packages:

  apt-get install ansible git

You will need the full source code for this repo on the starter node:

  git clone git@github.com:allisonrandal/tripleo-ansible.git
