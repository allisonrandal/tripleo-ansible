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

You will need to install Ansible on the starter node you used for your
TripleO deployment. It is recommended to use a source checkout of
Ansible method at the moment, because some packages on some distros
don't yet support needed features. The path is not significant, but
you may want to keep it next to tripleo-incubator::

  cd $TRIPLEO_ROOT
  git clone git://github.com/ansible/ansible.git

Set up the environment variables for operation of Ansible from the
source tree::

  cd $TRIPLEO_ROOT/ansible
  source ./hacking/env-setup

You may need to install some dependencies::

  sudo pip install paramiko PyYAML jinja2 httplib2
  sudo pip install oslo.config
  sudo pip install python-novaclient python-heatclient

Then clone a copy of this repo (again, the path is not significant)::

  cd $TRIPLEO_ROOT
  git clone git@github.com:allisonrandal/tripleo-ansible.git

Finally, copy one module from tripleo-ansible into the Ansible source
tree::

  cp $TRIPLEO_ROOT/tripleo-ansible/library/cloud/nova_rebuild \
     $TRIPLEO_ROOT/ansible/library/cloud/nova_rebuild

Simple Update
-------------

The best way to start understanding the Ansible update process is by
doing a simple single-node update. Make a copy of the Ansible
playbook examples/playbooks/simple_rebuild.yml, and update it with:

 * the credentials for your cloud
 * the name of the node you want to update
 * the new image_id to apply to the node
 * the option to preserve the ephemeral partition on the node

Then run the playbook to update the node::

  ansible-playbook simple_rebuild.yml -i $TRIPLEO_ROOT/tripleo-ansible/examples/hosts_local

The node will cycle through status REBUILD, then back to ACTIVE when
it is done updating. Note that rebuilds are slower with the
preserve_ephemeral option enabled.


The complete update playbooks add extra features, like pulling
metadata from Heat and the OS_* environment variables, and iterating
over all nodes in a cloud. But, starting with the simple update
highlights how cleanly and crisply the update feature is expressed
within Ansible.
