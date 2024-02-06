import flask, os, logging, subprocess, ua_parser

state = 'loud'
previous_state = 'loud'  # todo: read from file
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)


def usb_off():
    output = subprocess.check_output('sudo uhubctl -a off -l 1-1', shell=True)
    if not "off" in str(output):
        logging.error("Could not turn off USB")
        return False
    logging.debug("USB turned off")


def usb_on():
    subprocess.check_output('sudo uhubctl -a on -l 1-1', shell=True)
    if get_status == 'silent':
        logging.error("Could not turn on USB")
        return False
    logging.debug("USB turned on")


def get_status():
    # check if usb is on or off
    output = subprocess.check_output("sudo uhubctl -l 1-1", shell=True)
    if 'off' in str(output):
        return 'silent'
    else:
        return 'loud'


def get_user_agent():
    ua_string = flask.request.headers.get('User-Agent')
    logging.debug("User-Agent: " + ua_string)
    return ua_parser.user_agent_parser.Parse(ua_string)


def is_phone():
    user_agent = get_user_agent()
    if user_agent['os']['family'] == 'Other':
        logging.debug("Phone detected")
        return True
    else:
        logging.warning("Client is not a phone, denying request.")
        return False


if __name__ == "__main__":

    app = flask.Flask(__name__)

    @app.route('/silent')
    def silent():
        global state, previous_state
        logging.debug("Route /silent called")
        if not is_phone():
            return 'Access denied, you are not a Phone', 403
        usb_off()
        previous_state = state
        state = 'silent'
        logging.info("Silent mode on")
        return 'Silent mode on'


    @app.route('/loud')
    def loud():
        global state, previous_state
        logging.debug("Route /loud called")
        if not is_phone():
            return 'Access denied, you are not a Phone', 403
        usb_on()
        previous_state = state
        state = 'loud'
        logging.info("Silent mode off")
        return 'Silent mode off'


    @app.route('/restore')
    def restore():
        global state, previous_state
        logging.debug("Route /restore called")
        if not is_phone():
            return 'Access denied, you are not a Phone', 403
        if previous_state == 'loud':
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
        address = s.getsockname()[0]
        s.close()
        return address


    @app.route('/status')
    def status():
        return get_status()


    logging.info("Starting RadioSilence, ready to answer requests.")
    app.run(host='0.0.0.0', port=8080, debug=False)
