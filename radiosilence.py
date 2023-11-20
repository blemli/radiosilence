import flask, os, logging

def usb_off():
    # call uhubctl to turn off usb
    os.system('sudo uhubctl -a off -l 1-1')

def usb_on():
    # call uhubctl to turn on usb
    os.system('sudo uhubctl -a on -l 1-1')

if __name__ =="__main__":
    state='loud'
    previous_state='loud' # todo: read from file
    app = flask.Flask(__name__)
    @app.route('/silent')
    def silent():
        usb_off()
        previous_state=state
        state='silent'
        logging.info("Silent mode on")
        return 'Silent mode on'
    
    @app.route('/loud')
    def loud():
        usb_on()
        previous_state=state
        state='loud'
        logging.info("Silent mode off")
        return 'Silent mode off'
    
    @app.route('/restore')
    def restore():
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
        # check if usb is on or off
        import subprocess
        process = subprocess.Popen(['sudo', 'uhubctl', '-l', '1-1'], stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        if 'off' in stdout.decode('utf-8'):
            return 'silent'
        else:
            return 'loud'
        
    
    # start flask app
    app.run(host='0.0.0.0', port=8080, debug=False)
    
    