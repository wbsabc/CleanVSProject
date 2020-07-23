import os
import sys
import shutil

DELETE_FLAG = True #True-直接删除 | False-只打印删除文件路径
DELETE_VS = True
DELETE_SUO = True
DELETE_BIN = True
DELETE_OBJ = True
DELETE_USER = True

error_log = ''

def remove_file(path):
    global error_log
    try:
        if DELETE_FLAG:
            os.remove(path)
        print('Delete {0}'.format(path))
    except Exception as e:
        print(str(e))
        error_log = error_log + path + "\n"

def remove_dir(path):
    global error_log
    try:
        if DELETE_FLAG:
            shutil.rmtree(path)
        print('Delete {0}'.format(path))
    except Exception as e:
        print(str(e))
        error_log = error_log + path + "\n"

def output_log():
    global error_log
    if error_log != '':
        print("\n\nFailed Path:\n")
        print(error_log)

def judge_path(path):
    files = os.listdir(path)
    sln_level = False
    proj_level = False
    setup_level = False

    for f in files:
        if f.endswith('.sln'):
            sln_level = True
        if f.endswith('.csproj'):
            proj_level = True
        if f.endswith('.vddproj'):
            setup_level = True
    
    for f in files:
        is_dir = False
        if os.path.isdir(os.path.join(path, f)):
            is_dir = True
        if sln_level and DELETE_VS and f.lower() == '.vs' and is_dir:
            remove_dir(os.path.join(path, f))
            continue
        if sln_level and DELETE_SUO and f.lower().endswith('.suo') and not is_dir:
            remove_file(os.path.join(path, f))
            continue
        if proj_level and DELETE_BIN and f.lower() == 'bin' and is_dir:
            remove_dir(os.path.join(path, f))
            continue
        if proj_level and DELETE_OBJ and f.lower() == 'obj' and is_dir:
            remove_dir(os.path.join(path, f))
            continue
        if (sln_level or proj_level) and DELETE_USER and f.lower().endswith('.user') and not is_dir:
            remove_file(os.path.join(path, f))
            continue
        if setup_level and DELETE_BIN and (f.lower() == 'debug' or f.lower() == 'release') and is_dir:
            remove_dir(os.path.join(path, f))
            continue
        if is_dir:
            judge_path(os.path.join(path, f))

working_path = sys.argv[1]
if working_path.endswith('"'):
    working_path = working_path.replace('"', '\\')
print('Working Path: {0}\n'.format(working_path))
try:
    judge_path(working_path)
    output_log()
except Exception as e:
    print(str(e))

os.system('pause')
