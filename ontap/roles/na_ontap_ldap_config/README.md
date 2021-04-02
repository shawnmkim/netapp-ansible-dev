na_ontap_cluster_config
=========

Configure one or more of the following ONTAP settings:

Licenses
Aggregates
Ports
Interface Groups
VLANS
Broadcast Domains
Intercluster LIFs

Requirements
------------

Since this uses the NetApp ONTAP modules it will require the python library netapp-lib

Role Variables
--------------

hostname: <ONTAP mgmt ip or fqdn>
username: <ONTAP admin account>
password: <ONTAP admin account password>

Based on if Variables != or == None determins if a section runs.  Each variable will take one or more dictonary entries.  The following would run all sections

license_codes: AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAA,AAAAAAAAAAAAAA

aggrs:
  - { name: aggr1, node: vsim-01, disk_count: 26, max_raid: 26 }
  - { name: aggr2, node: vsim-02, disk_count: 26, max_raid: 26 }

ports:   #* Ports also has variables 'autonegotiate', and 'flowcontrol' which default to true, and none but can be overriden by your playbook
  - { node: vsim-01, port: e0c, mtu: 9000 }

ifgrps:
  - { name: a0a, node: vsim-01, port: "e0a", mode: multimode }
  - { name: a0a, node: vsim-02, port: "e0a", mode: multimode }
  - { name: a0a, node: vsim-01, port: "e0b", mode: multimode }
  - { name: a0a, node: vsim-02, port: "e0b", mode: multimode }

vlans:
  - { id: 201, node: vsim-01, parent: a0a }

bcasts:
  - { name: Backup, mtu: 9000, ipspace: default, ports: 'vsim-01:e0c,vsim-02:e0c' }

inters:
  - { name: intercluster_1, address: 172.32.0.187, netmask: 255.255.255.0, node: vsim-01, port: e0c }
  - { name: intercluster_2, address: 172.32.0.188, netmask: 255.255.255.0, node: vsim-02, port: e0c }

cluster_name: vsim  # needs to be set for the vserver that the interclusters will go on.

Dependencies
------------

None

Example Playbook
----------------

I use a globals file to hold my variables.

globals.yml
cluster_name: vsim

netapp_hostname: 172.32.0.182
netapp_username: admin
netapp_password: netapp123

license_codes: <removed>

aggrs:
  - { name: aggr1, node: vsim-01, disk_count: 26, max_raid: 26 }
  - { name: aggr2, node: vsim-02, disk_count: 26, max_raid: 26 }

ifgrps:
  - { name: a0a, node: vsim-01, port: "e0a", mode: multimode }
  - { name: a0a, node: vsim-02, port: "e0a", mode: multimode }
  - { name: a0a, node: vsim-01, port: "e0b", mode: multimode }
  - { name: a0a, node: vsim-02, port: "e0b", mode: multimode }

inters:
  - { name: intercluster_1, address: 172.32.0.187, netmask: 255.255.255.0, node: vsim-01, port: e0c }
  - { name: intercluster_2, address: 172.32.0.188, netmask: 255.255.255.0, node: vsim-02, port: e0c }

cluster_config.yml
---
- hosts: localhost
  vars_files:
    - globals.yml
  vars:
    input: &input
      hostname: "{{ netapp_hostname }}"
      username: "{{ netapp_username }}"
      password: "{{ netapp_password }}"
  tasks:
  - import_role:
      name: schmots1.na_ontap_cluster_config
    vars:
      <<: *input

License
-------

GNU v3

Author Information
------------------
NetApp
http://www.netapp.io
