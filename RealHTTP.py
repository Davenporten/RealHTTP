#!/usr/bin/python
# Filename: REALHTTP.py

class RealHTTP:
    def __init__(self):
        self.PARTIAL = 1
        self.FULL = 2
        self.FAIL = 4
        self.content = ''
        self.request_type = None # This will be a string
        self.url = None
        self.version = None
        self.headers = {}
        self.body = None
        self.needed_body = 0
        self.error = None
        self.status = 'No status'
        self.ERR1 = 1 # Signifies that there was no request method

    def PARTIAL(self):
        return self.PARTIAL

    def FULL(self):
        return self.FULL

    def FAIL(self):
        '''This will be used mostly for when someone calls getMessage() when there is not a full message.'''
        return self.FAIL

    def execute(self, data):
        '''Main functionality of the parser, checks if there is a complete http message; parses through the message if it's complete and returns from the function making all the data as the remainder content.'''
        data = self.content + data
        self.content = ''

        # Attempts to split the data based on the terminating characters of an http message.
        # If there are more than 1 elements in the list there is a complete message.
        message = data.split('\r\n\r\n',1)
        if len(message) == 1:
            self.content = self.content + data
            return self.PARTIAL

        # Goes through whatever wasn't a part of the first http request and puts it into the remainder content inserting '\r\n\r\n' where appropriate in case of multiple complete http requests
        int i = 1
        while i < len(message):
            self.content = self.content + message[i]
            if not (i == (len(message) - 1)):
                self.content = self.content + '\r\n\r\n'
            i = i + 1

        # Splits the http request into separate lines.
        # Each line is then split 
        lines = message[0].split('\r\n')
        for l in lines:
            if l == '':
                continue
            broke = l.split(':',1)
            if len(broke) == 2:
                self.headers[broke[0]] = broke[1]
            elif len(broke) == 1:
                first = broke[0].split()
                if len(first) == 3:
                    self.request_type = first[0]
                    self.url = first[1]
                    self.version = first[2]
                else:
                    for f in first:
                        if f[:1] == '/':
                            self.url = f
                        elif f[:4] == 'HTTP':
                            self.version = f
                        else:
                            self.request_type = f  
            else:
                return self.FAIL
        return self.FULL
 
    #def execute_entity(self, data):
    
    def full_message(self):
        '''Returns true if there is a full message and false if not; type will be None if there is not a full message.'''
        if self.request_type:
            return True
        return False

    def get_request_type(self):
        '''Returns the request type (GET, POST, etc) or None if there is not a full message.'''
        return self.request_type

    def get_url(self):
        '''Returns the urls of the request or None if there is not a full message.'''
        return self.url

    def get_version(self):
        '''Returns the HTTP version of the request or None if there is not a full message.'''
        return self.version

    def get_headers(self):
        '''Returns the headers of the message or None if there is not a full message.'''
        return self.headers

    def get_remainder(self):
        '''Returns all the unused data that was received but not included in a message (for caching).'''
        return self.content

    def get_body(self):
        '''Returns the entity body if there is one; returns None if there isn't one or if the message isn't full.'''
        return self.body

    def get_error(self):
        '''Returns the error message if FAIL is ever returned.'''
        return self.error

    def get_status(self):
        '''Returns a message indicating what happened that last time execute was called and the start of the request.'''
        return self.status

version = '0.1'

# End of REALHTTP.py
