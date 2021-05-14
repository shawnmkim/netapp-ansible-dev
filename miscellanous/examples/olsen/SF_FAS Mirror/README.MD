Update Hostinfo.yml and Globals.yml 

Create sfsecret.yml which contains 
hostname: Mysfhost or ip (MVIP)
username: My-SF-User
password: my-sf-Password
netapp_hostname: mynetapp or ip (Cluster IP or name)
netapp_username: MyNetapp_user 
netapp_password: MyNetapppassword


This Playbook does the following.
  1. Creates new Account for Database Server
  2. Creates Desired number of Data volumes on solidfire 0 == OK (state==absent for delete)
  3. Creates Desired number of Log volumes on solidfire 0 == OK (state==absent for delete)
  4. Creates Desired number of Biniary Volumes On solidfire 0 == OK (state==absent for delete)
  5. Creates Host Access Group with DB-host-name
  6. Creates QOS Policy with DB-host-name
  7. Sets QOS Policy for all volumes to QOS Policy and Enables Snapmirror to fas on volumes
  8. Delete QOS if state == absent
  9. Creates Access group
  10. Deletes Access group if state == absent
  11. Adds volumes to Access group
All steps below this point will only occur if mirrored == true (default)
  12. FAS Side Creates or verifies SVM
  13. Create or Verify Snapmirror Peer is created SF and FAS
  14. Get Snapmirrors for delete if state == absent
  15. Set up snapshot schedule on SF
  16. Remove Snapmirror relationships if state == absent
  17. Delete snapshot schedule if state == absent
  18. Create/Delete FAS volumes Data
  19. Create/Delete FAS volumes LOG
  20. Create/Delete FAS volumes bin
  21. Create snapshot schedule with Mirror update label
  22. Setup new connection between SF and FAS if required
  23. Create Relationships
  24. Intialize relationships
  25. 


