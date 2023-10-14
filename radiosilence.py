import flask, os

def usb_off():
    # call uhubctl to turn off usb
    os.system('sudo uhubctl -a off -l 1-1')

def usb_on():
    # call uhubctl to turn on usb
    os.system('sudo uhubctl -a on -l 1-1')

if __name__ =="__main__":
    # create flask app
    app = flask.Flask(__name__)
    # define app routes
    @app.route('/silent')
    def silent():
        usb_off()
        return 'Silent mode on'
    
    @app.route('/loud')
    def loud():
        usb_on()
        return 'Silent mode off'
    

    # start flask app
    app.run(host='0.0.0.0', port=8080, debug=False)

