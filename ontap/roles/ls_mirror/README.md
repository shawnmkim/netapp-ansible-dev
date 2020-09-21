Role Name
=========

This role creates a load-sharing mirror for the SVM_root

Requirements
------------

This role is dependant upon an SVM having been previously created. 

Role Variables
--------------

---
# defaults file for ls_mirror
ls_mirrors:
    - { ls_source_volume: "{{ svm }}_root", 
        size: 1, 
        size_unit: gb, 
        source_svm: "{{ svm }}", 
        ls_destination_volume: "{{ svm }}_root_LS", 
        destination_svm: "{{ svm }}", 
        destination_aggregate: "aggr_data1", 
        schedule: "5min", 
        lsupdate: "N" }

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

Originally developed by John Champion. 
Adapted by Ken Hillier.
