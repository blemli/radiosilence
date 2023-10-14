import flask, os, logging

def usb_off():
    # call uhubctl to turn off usb
    os.system('sudo uhubctl -a off -l 1-1')

def usb_on():
    # call uhubctl to turn on usb
    os.system('sudo uhubctl -a on -l 1-1')

if __name__ =="__main__":
    app = flask.Flask(__name__)
    @app.route('/silent')
    def silent():
        usb_off()
        logging.info("Silent mode on")
        return 'Silent mode on'
    
    @app.route('/loud')
    def loud():
        usb_on()
        logging.info("Silent mode off")
        return 'Silent mode off'
    
    # start flask app
    app.run(host='0.0.0.0', port=8080, debug=False)

