#!/usr/bin/python
# Filename: RealHTTP.py

class RealHTTP:
    def __init__(self):
        # Return values for how the parsing went
        self.PARTIAL = 1
        self.FULL = 2
        self.FAIL = 4
        # ~~~~~~~~~~~~~~
        self.content = ''        # The remainder data after the data is parsed
        self.request_type = None
        self.url = None
        self.version = None
        self.headers = {}       # A dict of all the headers; key: header, value: whatever the header's value is
        self.body = ''          # Entity body of the request; if there is one
        self.needed_body = 0    # The number of bytes still needed for the entity body
        self.error = None       # If there parsing fails for any reason a string is put in to explain why
        self.start = 1 # This is an important line, it's used to for proper formatting of the headers and avoiding overriding correct data; if it has already done the first like of the request and tried to do it again it will skip that header.

    def clear(self):
        '''Resets all data members to what they would be at time of initialization.'''
        self.content = ''
        self.request_type = None
        self.url = None
        self.version = None
        self.headers.clear()
        self.body = ''
        self.needed_body = 0
        self.error = None
        self.start = 1

    '''Not sure if these will be particularly useful, but they can be called if someone wants.'''
    def PARTIAL(self):
        return self.PARTIAL

    def FULL(self):
        return self.FULL

    def FAIL(self):
        return self.FAIL
    # ~~~~~~~~~~~~~~~~~~~~

    def execute(self, data):
        '''Main functionality of the parser, checks if there is a complete http message; parses through the message if it's complete and returns from the function making all the data as the remainder content.'''
        data = self.content + data
        if not data:
            self.error = 'There was no data in the parser\'s remainder and no data was passed in.'
            return self.FAIL
        self.content = ''

        # Attempts to split the data based on the terminating characters of an http message.
        # If there are more than 1 elements in the list there is a complete message.
        message = data.split('\r\n\r\n',1)
        if len(message) == 1:
            self.content = self.content + data
            return self.PARTIAL

        # Goes through whatever wasn't a part of the first http request and puts it into the remainder content inserting '\r\n\r\n' where appropriate in case of multiple complete http requests
        i = 1
        while i < len(message):
            self.content = self.content + message[i]
            if not (i == (len(message) - 1)):
                self.content = self.content + '\r\n\r\n'
            i = i + 1

        # Splits the http request into separate lines.
        # Each line is then split by the first ':'; if there are two elements it is added to the headers, if there is one it is the first line of the request, and if there is anything else the message is bad
        lines = message[0].split('\r\n')
        for l in lines:
            if l == '':
                continue
            broke = l.split(':',1)
            if len(broke) == 2:
                self.headers[broke[0]] = broke[1]
                # I feel like there must be a better way of doing thing
                head = broke[0].lower()
                if head == 'content-length':
                    self.needed_body = int(broke[1])
                # ~~~~~~~~~~~~~
            elif len(broke) == 1:
                first = broke[0].split()
                if len(first) == 3 and self.start:
                    self.request_type = first[0]
                    self.url = first[1]
                    self.version = first[2]
                    self.start = 0 # First line is being done, it should never get back in here
                elif self.start:
                    self.start = 0 # First line is being done, it should never get back in here
                    for f in first:
                        if f[:1] == '/':
                            self.url = f
                        elif f[:4] == 'HTTP':
                            self.version = f
                        elif '/' in f:
                            self.error = 'Request was ill formatted.'
                            return self.FAIL
                        else:
                            self.request_type = f  
            else:
                self.error = 'Unrecognized error, the request my be empty.'
                return self.FAIL
        return self.FULL

    def execute_body(self, data):
        '''Parses the data to construct the entity body based on the content-length, returning FULL, PARTIAL, or FAIL.'''
        data = self.content + data
        if self.needed_body > len(data):
            self.body = self.body + data
            self.needed_body = self.needed_body - len(data)
            if self.needed_body:
                return self.PARTIAL
            else:
                return self.FULL
        self.body = self.body + data[:self.needed_body]
        self.needed_body = 0
        return self.FULL
 
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

    def test(self,request):
        '''A simple function for testing, not really useful in actually using the parser, but is more for developing the parser. Takes in a request message, calls execute, prints out relevant data members, tries to parse the entity body and prints out the body if there is one.'''

        result = self.execute(request)
        if result == self.FULL:
            print 'FULL'
        if result == self.PARTIAL:
            print 'PARTIAL'
        if result == self.FAIL:
            print 'FAIL'

        print 'Headers: ' + str(self.get_headers())
        print 'Type: ' + str(self.get_request_type())
        print 'Url: ' + str(self.get_url())
        print 'Version: ' + str(self.get_version())
        print 'Remainder: ' + str(self.get_remainder())
        print 'Error: ' + str(self.get_error())
        print 'Calling execute_body()'
        f.execute_body(self.get_remainder())
        print 'Entity body: ' + str(self.get_body())
        print '\n'

version = '0.1'

# End of RealHTTP.py
