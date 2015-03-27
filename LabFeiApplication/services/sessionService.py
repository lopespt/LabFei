__author__ = 'wachs'


class Session(dict):

    def printAttributes(self):
        print(self.__dict__)

sessions = {}


def add_session(session_id):
    if not session_id in sessions:
        sessions[session_id] = Session()
        printSessions()


def get_session(session_id):
    if session_id in sessions:
        printSessions()
        return sessions[session_id]
    else:
        return None

def printSessions():
    for k in sessions.keys():
        print(sessions[k].printAttributes())

def logged_user(request):
    if 'logged_user' in request.session:
        return request.session['logged_user']
    else:
        return None
