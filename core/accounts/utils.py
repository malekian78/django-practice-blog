import threading

# this class will not get used in dev phase , because email backend is console
class EmailThreading(threading.Thread):

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self) -> None:
        self.email_obj.send()
