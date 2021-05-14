import glob
import subprocess
import re
import sys
import os

def return_options(modulename='na_ontap_volume', required_exclude=['hostname','password','username'], optional_exclude=['https','validate_certs','use_rest','http_port','ontapi','username','password','cert_filepath','key_filepath','debug']):
    output = subprocess.run(['ansible-doc', modulename], capture_output=True)
    collvar = {}
    collvar['required'] = []
    collvar['optional'] = []
    for x in output.stdout.decode('utf-8').split("\n"):
        n = re.findall(r'^= (\w+)',x)
        if n and n[0] not in required_exclude:
            collvar['required'].append(n[0])
            
    for x in output.stdout.decode('utf-8').split("\n"):
        n = re.findall(r'^- (\w+)',x)
        excludelist = optional_exclude + collvar['required']
        if n and n[0] not in excludelist:
            collvar['optional'].append(n[0])
    collvar['optional'] = set(collvar['optional'])
    return collvar

def write_mods_to_files(commands, filepath="/Users/john/Documents/GitHub/netapp_ansible_collections_templates/"):
    # Write out Tasks
    for key in sorted (commands):
        f = open('{}tasks/{}_task.yml'.format(filepath,key),"w+")
        f.write('---\n- name: Running command {}\n  {}:\n'.format(key,key))
        f.write('    hostname: "{{ netapp_hostname }}"\n    username: "{{ netapp_username }}"\n    password: "{{ netapp_password }}"\n    https: "{{ netapp_https | default(true) }}"\n    port: "{{ netapp_port | default(omit) }}"\n    validate_certs: "{{ validate_certs | default(false) }}"\n')
        
        for value in sorted (commands[key]['required']):
            f.write("    {1}: '{{{{ {0}_{1}_01 }}}}'\n".format(key.replace('na_ontap_','req_').replace('na_elementsw_','req_'),value) )
    
        for value in sorted (commands[key]['optional']):
            f.write("    {1}: '{{{{ {0}_{1}_01 | default(omit) }}}}'\n".format(key.replace('na_ontap_','opt_').replace('na_elementsw_','opt_'),value))
        
        f.write("  register: results\n")
        f.closed
    for key in sorted (commands):
        f = open('{}play/{}_play.yml'.format(filepath,key),"w+")
        f.write('    - name: Running command {}\n      include_task: tasks/{}_task.yml\n'.format(key,key))
        f.closed

    for key in sorted (commands):
        f = open('{}play/{}_play.yml'.format(filepath,key),"w+")
        f.write('    - name: Running command {}\n      include_task: tasks/{}_task.yml\n'.format(key,key))
        f.closed

    for key in sorted (commands):
        f = open('{}tasks/multi_{}_task.yml'.format(filepath,key),"w+")
        f.write('---\n- name: Running command {}\n  {}:\n'.format(key,key))
        f.write('    hostname: "{{ netapp_hostname }}"\n    username: "{{ netapp_username }}"\n    password: "{{ netapp_password }}"\n    https: "{{ netapp_https | default(true) }}"\n    port: "{{ netapp_port | default(omit) }}"\n    validate_certs: "{{ validate_certs | default(false) }}"\n')
        
        for value in sorted (commands[key]['required']):
            f.write("    {1}: 'item.{{{{ {0}_{1}_01 }}}}'\n".format(key.replace('na_ontap_','req_').replace('na_elementsw_','req_'),value) )
    
        for value in sorted (commands[key]['optional']):
            f.write("    {1}: 'item.{{{{ {0}_{1}_01 | default(omit) }}}}'\n".format(key.replace('na_ontap_','opt_').replace('na_elementsw_','opt_'),value))
        
        f.write("  register: results\n")
        f.closed


    # Write out Varibles
    for key in sorted (commands):
        f = open('{}vars/{}_vars.yml'.format(filepath,key),"w+")
        f.write('\n    #vars:\n# Section: {}:\n'.format(key))
        f.write('    hostname: "{{ netapp_hostname }}"\n    username: "{{ netapp_username }}"\n    password: "{{ netapp_password }}"\n    https: "{{ netapp_https | default(true) }}"\n    port: "{{ netapp_port | default(omit) }}"\n    validate_certs: "{{ validate_certs | default(false) }}"\n')
        for value in sorted (commands[key]['required']):
            f.write("    {1}: '{{{{ {0}_{1}_01 }}}}'\n".format(key.replace('na_ontap_','req_').replace('na_elementsw_','req_'),value))
        for value in sorted (commands[key]['optional']):
            f.write("    #{1}: '{{{{ {0}_{1}_01 | default(omit) }}}}'\n".format(key.replace('na_ontap_','opt_').replace('na_elementsw_','opt_'),value))
        f.write("  \n")
        f.closed

commands = {}
oscommands = {}
workingpath = "./"
# Update the ontap 
print("Updating Modules:")
subprocess.run(['ansible-galaxy','collection','install','-f','netapp.ontap'], capture_output=False)
# OldSchool
osfilepath = '/Users/john/anaconda3/lib/python3.7/site-packages/ansible/modules/storage/netapp/na_*.py'
filepath = '/Users/john/.ansible/collections/ansible_collections/netapp/ontap/plugins/modules/na_*.py'

print("Collecting Module data:")
for f in glob.glob(filepath):
    f = f.split('/')[-1].replace(".py","")
    module = "netapp.ontap.{}".format(f)
    sys.stdout.write("-")
    sys.stdout.flush()
    oscommands[f] = return_options(f)
    commands[f] = return_options(module)

#print(commands)
for x in ["play","tasks","vars"]:
  if not os.path.exists(workingpath+x):
    print("Creating ",x)
    os.makedirs(workingpath+x)

write_mods_to_files(commands,"./")
 

