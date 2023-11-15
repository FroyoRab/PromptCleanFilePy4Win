import os
import sys
import time
from loguru import logger

logger.add('__clear.log')

def get_del_file_list(base_dir,day)->list:
    t = day * 24 * 60 * 60
    #获取文件夹下所有文件和文件夹
    return_list = []
    files = os.listdir(base_dir)
    for file in files:
        filePath = base_dir + "/" + file
        #判断是否是文件
        if os.path.isfile(filePath):
            # 避开脚本
            if filePath.find("__clear.py")!=-1:continue
            if filePath.find("__clear.log")!=-1:continue
            #最后一次修改的时间
            last = int(os.stat(filePath).st_mtime)
            #上一次访问的时间
            #last = int(os.stat(filePath).st_atime)
            #当前时间
            now = int(time.time())
            #删除过期文件
            if (now - last >= t):
                return_list.append(os.path.abspath(filePath))
                # os.remove(filePath)
                # print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            #如果是文件夹，继续遍历删除
            return_list += get_del_file_list(filePath,day)
            #如果是空文件夹，删除空文件夹
            if not os.listdir(filePath):
                return_list.append(filePath)
    return return_list


def del_list_file(file_list:list):
    deled_file_list = []
    for one_file in file_list:
        os.remove(one_file)
        deled_file_list.append(one_file)
        logger.info(one_file)
    return deled_file_list
        
from winsdk_toast import Notifier, Toast
from winsdk_toast.event import EventArgsActivated
def handle_activated(event_args_activated: EventArgsActivated):
    if event_args_activated.argument=='snooze':
        global FILE_LIST
        deleds = del_list_file(FILE_LIST)
        send_win_toast(title='🍃 清理结果 🍃',message='\n'.join(deleds),action=False)
    else : pass

def send_win_toast(title,message,action:bool):
    notifier = Notifier('Python[template_clear/__clear.py]')
    toast = Toast()
    toast.add_text(title,hint_align='center', hint_style='caption')
    toast.add_text(message)
    if action:
        toast.add_action('✨ 确认 ✨',activationType='system',arguments='snooze')
        toast.add_action('❌ 取消 ❌',activationType='system',arguments='dismiss')
        notifier.show(toast,handle_activated=handle_activated)
    else: 
        notifier.show(toast)

@logger.catch
def run(base_dir,day=7):
    global FILE_LIST
    FILE_LIST = get_del_file_list(base_dir,day)
    if not FILE_LIST:
        send_win_toast('🍃 定时清理文件 🍃',"✔️ 本次无文件需要清理 ✔️")
        return
    file_list_str = '\n'.join(FILE_LIST)
    send_win_toast('🍃 定时清理文件 🍃', f"以下文件即将删除：\n{file_list_str}",action=True)
    
    
if __name__ == "__main__":
    run('O:\\Download\\_____template_clear_____')