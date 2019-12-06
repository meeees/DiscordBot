from flask import Flask, request
import os
import asyncio
import traceback
import sys

app = Flask('app_update')
update_cmd = 'sh app_update.sh'
# if this has been started by another python process, this will be False and update_cmd will be a lambda function
update_cmd_shell = True
update_coroutine_loop = None

@app.route('/git', methods=['POST'])
def get_webhook_post(): 
    try :
        json = request.get_json()
        ref = json['ref']
        # run the command
        if ref.endswith('master') :
            # run a shell script
            if update_cmd_shell :
                os.system(update_cmd)
            # or run an async function
            else :
				os.system(update_cmd)
                future = asyncio.run_coroutine_threadsafe(update_cmd(), update_coroutine_loop)
                future.result()

            print('Update command run')
        return '204'
    except Exception :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print ('Error reading from webhook')
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return '500'
        

def python_start(update_fnc, update_loop) :
    global update_cmd
    global update_cmd_shell
    global update_coroutine_loop
    update_cmd = update_fnc
    update_cmd_shell = False
    update_coroutine_loop = update_loop
    app.run(host='0.0.0.0')

if __name__ == '__main__' : 
    app.run(host='0.0.0.0')
