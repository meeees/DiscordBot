from flask import Flask, request
import os

app = Flask('app_update')
update_cmd = 'sh app_update.sh'
# if this has been started by another python process, this will be False and update_cmd will be a lambda function
update_cmd_shell = True

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
            # or run a lambda function
            else :
                update_cmd()

            print('Update command run')
        return '204'
    except Exception as e :
        print ('Error reading from webhook')
        print (e)
        

def python_start(update_fnc) :
    update_cmd = update_fnc
    update_cmd_shell = False
    app.run(host='0.0.0.0')

if __name__ == '__main__' : 
    app.run(host='0.0.0.0')