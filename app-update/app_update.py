from flask import Flask, request
import os

app = Flask('app_update')
update_cmd = 'sh app_update.sh'

@app.route('/git', methods=['POST'])
def get_webhook_post(): 
    json = request.get_json()
    ref = json['ref']
    # run the command
    if ref.endswith('master') :
        os.system(update_cmd)
        print('Application restarted')
    return '204'

if __name__ == '__main__' : 
    app.run(host='0.0.0.0')
