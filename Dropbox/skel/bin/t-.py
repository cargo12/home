#!/usr/bin/python

import warnings
warnings.filterwarnings('ignore', 'the md5 module is deprecated')

import os, sys, md5, random

def hash(x): return md5.md5(x).hexdigest()[:4]

def read_task_file(filename):
    try: tasks = [ t for t in file(filename).read().split('\n') if t]
    except: tasks = []
    return tasks

def save_tasks_file(filename,task_list):
    try: os.rename(filename,filename+'_bkp')
    except: pass
    task_list.sort()
    file(filename,'w').write(''.join([t+'\n' for t in task_list if t]))

args           =  sys.argv[1:]
task_to_remove =  'No task to remove'
task_spec      =  []
tasks          =  []

while args:

    arg = args.pop(0)
    if arg=='--help' or arg=='-h':
        print """

    Overly simplistic tasks list:
    
        --help or -h         : Print this file
        --task-dir    <dir>  : Directory for the tasks file
        --list        <file> : The tasks file
        --recover            : Restore previous task list
                               (Only works once)
        -f            <hash> : Finished task <hash>
        -f            x      : Remove remembered finished tasks
        <task to add>
    
    With no arguments, print the list of tasks
        in random order, deleted tasks last.

"""
        sys.exit()

    if arg=='--recover':
        filename = task_dir+'/'+task_file
        os.rename(filename+'_bkp',filename)
        break

    if arg=='--task-dir': task_dir       = args.pop(0)         ; continue
    if arg=='--list'    : task_file      = args.pop(0)         ; continue
    if arg=='-f'        : task_to_remove = args.pop(0) + ' : ' ; continue

    task_spec.append(arg)

for t in read_task_file(task_dir+'/'+task_file):

    if t.startswith(task_to_remove):
        if task_to_remove=='x : ': continue
        t = 'x : ' + t
        task_to_remove = 'zzzz'
    tasks.append(t)

new_task_string = ' '.join(task_spec)

if new_task_string:
    tasks.append(hash(new_task_string)+' : '+new_task_string)

if new_task_string or task_to_remove!='No task to remove':
    save_tasks_file(task_dir+'/'+task_file,tasks)

random.shuffle(tasks)
print '\n'.join([ t for t in tasks if not t.startswith('x : ')])
print '\n'.join([ t for t in tasks if     t.startswith('x : ')])

