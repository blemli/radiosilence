import flask, os, logging,subprocess
state='loud'
previous_state='loud' # todo: read from file
import subprocess
def usb_off():
    # call uhubctl to turn off usb
    os.system('sudo uhubctl -a off -l 1-1')
    


def usb_on():
    # call uhubctl to turn on usb
    os.system('sudo uhubctl -a on -l 1-1')

def get_status():
    # check if usb is on or off
    output = subprocess.check_output("sudo uhubctl -l 1-1", shell=True)
    if 'off' in str(output):
        return 'silent'
    else:
        return 'loud'

if __name__ =="__main__":

    app = flask.Flask(__name__)
    @app.route('/silent')
    def silent():
        user_agent = flask.request.headers.get('User-Agent')
        logging.info(f"User-Agent: {user_agent}")
        print(f"User-Agent: {user_agent}")
        global state, previous_state
        usb_off()
        previous_state=state
        state='silent'
        logging.info("Silent mode on")
        return 'Silent mode on'
    
    @app.route('/loud')
    def loud():
        global state, previous_state
        usb_on()
        previous_state=state
        state='loud'
        logging.info("Silent mode off")
        return 'Silent mode off'
    
    @app.route('/restore')
    def restore():
        global state, previous_state
        if previous_state=='loud':
            usb_on()
            logging.info("Restored to loud")
            return "Restored to loud"
        else:
            logging.info("Keeping silent")
            return "Keeping silent"
        
    
    @app.route('/ip')
    def ip():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
        s.close()
        return ip
    
    @app.route('/status')
    def status():
        return get_status()
    
    # start flask app
    app.run(host='0.0.0.0', port=8080, debug=False)
    
    