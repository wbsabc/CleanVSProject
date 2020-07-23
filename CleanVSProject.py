import os
import sys
import shutil

DELETE_FLAG = True #True-直接删除 | False-只打印删除文件路径
DELETE_VS = True
DELETE_SUO = True
DELETE_BIN = True
DELETE_OBJ = True
DELETE_USER = True

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
            if DELETE_FLAG:
                shutil.rmtree(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if sln_level and DELETE_SUO and f.lower().endswith('.suo') and not is_dir:
            if DELETE_FLAG:
                os.remove(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if proj_level and DELETE_BIN and f.lower() == 'bin' and is_dir:
            if DELETE_FLAG:
                shutil.rmtree(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if proj_level and DELETE_OBJ and f.lower() == 'obj' and is_dir:
            if DELETE_FLAG:
                shutil.rmtree(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if (sln_level or proj_level) and DELETE_USER and f.lower().endswith('.user') and not is_dir:
            if DELETE_FLAG:
                os.remove(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if setup_level and DELETE_BIN and (f.lower() == 'debug' or f.lower() == 'release') and is_dir:
            if DELETE_FLAG:
                shutil.rmtree(os.path.join(path, f))
            print('Delete {0}'.format(os.path.join(path, f)))
            continue
        if is_dir:
            judge_path(os.path.join(path, f))
        
print('Working Path: {0}'.format(sys.argv[1]))
try:
    judge_path(sys.argv[1])
except Exception as e:
    print(str(e))

os.system('pause')
