import flask, os, logging, subprocess
import threading
from ua_parser import user_agent_parser
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)


lock = threading.Lock()
state = 'loud'
previous_state = state


def get_status():
    # check if usb is on or off
    output = subprocess.check_output("uhubctl -l 1-1", shell=True)
    if 'off' in str(output):
        return 'silent'
    else:
        return 'loud'


def usb_off():
    with lock:
        output = subprocess.check_output('uhubctl -a off -l 1-1', shell=True)
        if not "off" in str(output):
            logging.error("Could not turn off USB")
            return False
        logging.debug("USB turned off")


def usb_on():
    with lock:
        subprocess.check_output('uhubctl -a on -l 1-1', shell=True)
        if get_status() == 'silent':
            logging.error("Could not turn on USB")
            return False
        logging.debug("USB turned on")


def get_user_agent():
    ua_string = flask.request.headers.get('User-Agent')
    logging.debug("User-Agent: " + ua_string)
    return user_agent_parser.Parse(ua_string)


def is_phone():
    user_agent = get_user_agent()
    if user_agent['os']['family'] == 'Other':
        logging.debug("Phone detected")
        return True
    else:
        logging.warning("Client is not a phone, denying request.")
        return False

def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # it works even if 8.8.8.8 is not reachable
    address = s.getsockname()[0]
    s.close()
    return address


if __name__ == "__main__":

    app = flask.Flask(__name__)
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="memory://",
    )


    @app.route('/silent')
    @limiter.limit("3 per second, 5 per 10 seconds, 15 per minute")
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
    @limiter.limit("3 per second, 5 per 10 seconds, 15 per minute")
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


    # @app.route('/restore')
    # @limiter.limit("3 per second, 5 per 10 seconds, 15 per minute")
    # def restore():
    #     global state, previous_state
    #     logging.debug("Route /restore called")
    #     if not is_phone():
    #         return 'Access denied, you are not a Phone', 403
    #     if previous_state == 'loud':
    #         usb_on()
    #         state = 'loud'
    #         logging.info("Restored to loud")
    #         return "Restored to loud"
    #     else:
    #         state = 'silent'
    #         logging.info("Keeping silent")
    #         return "Keeping silent"


    @app.route('/ip')
    def ip():
        address = get_ip()
        return address


    @app.route('/status')
    def status():
        return get_status()


    logging.info("Starting RadioSilence, ready to answer requests.")
    logging.info("connect to http://radiosilence.local or  http://" + get_ip())
    app.run(host='0.0.0.0', port=8080, debug=False)
