# -*- coding: utf-8 -*-
# created by vince67 Feb.2014
# nuovince@gmail.com

import re
import os
import subprocess


def run(project_dir, date_from, date_to, search_key, filename):
    bug_dic = {}
    bug_branch_dic = {}
    try:
        os.chdir(project_dir)
    except Exception, e:
        raise e
    branches_list = []
    branches_list = get_branches()
    for branch in branches_list:
        bug_branch_dic = deal_branch(date_from,
                                     date_to,
                                     branch,
                                     search_key)
        for item in bug_branch_dic:
            if item not in bug_dic:
                bug_dic[item] = bug_branch_dic[item]
            else:
                bug_dic[item] += bug_branch_dic[item]
    log_output(filename, bug_dic)


# abstract log of one branch
def deal_branch(date_from, date_to, branch, search_key):
    try:
        os.system('git checkout ' + branch)
        os.system('git pull ')
    except Exception, error:
        print error
    cmd_git_log = ["git",
                   "log",
                   "--stat",
                   "--no-merges",
                   "-m",
                   "--after="+date_from,
                   "--before="+date_to]
    proc = subprocess.Popen(cmd_git_log,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    bug_branch_dic = deal_lines(date_from,
                                date_to,
                                search_key,
                                stdout)
    return bug_branch_dic

# write commits log to file
def log_output(filename, bug_dic):
    fi = open(filename, 'w')
    for item in bug_dic:
        m1 = '--'*5 + 'BUG:' + item + '--'*20 + '\n'
        fi.write(m1)
        for commit in bug_dic[item]:
            fi.write(commit)
    fi.close()


# analyze log
def deal_lines(date_from, date_to, search_key, stdout):
    bug_dic = {}
    for line in stdout.split('commit '):
        if re.search('Bug: \d+', line) is not None and re.search(search_key, line) is not None:
            bug_id = line.split('Bug: ')[1].split('\n')[0]
            if bug_id not in bug_dic:
                bug_dic[bug_id] = [line]
            else:
                bug_dic[bug_id] += [line]
    return bug_dic


# get all branches of a project
def get_branches():
    branch_list = []
    branches = []
    tmp_str = ''
    try:
        cmd_git_remote = 'git remote show origin'
        proc = subprocess.Popen(cmd_git_remote.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        tmp_str = stdout.split('Local branches configured')[0]
        try:
            tmp_str = tmp_str.split('Remote branches:\n')[1]
        except:
            tmp_str = tmp_str.split('Remote branch:\n')[1]
        branches = tmp_str.split('\n')
        for branch in branches[0:-1]:
            if re.search(' tracked', branch) is not None:
                branch = branch.replace('tracked', '').strip(' ')
                branch_list.append(branch)
    except Exception, error:
        if branch_list == []:
            print "Can not get any branch!"
    return branch_list


if __name__ == '__main__':
    # path of the .git project. example: "/home/username/projects/jekyll_vincent"
    project_dir = ""
    date_from = "2014-01-25"
    date_to = "2014-02-26"
    # only search 'Bug: \d+' for default
    search_key = ""
    # name of output file. example:"/home/username/jekyll_0125_0226.log"
    filename = ""
    run(project_dir, date_from, date_to, search_key, filename)