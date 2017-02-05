# RealHTTP - An HTTP parser

While there are other parsers, I created RealHTTP because I've been really dissatisfied with what's out there, particularly with poorly named functions and lack of documentation. With RealHTTP I'm hoping it's a parser that is intuitive to use and one with easy to read documentation (found below). There are some comments in the code to help explain the use and implementation of the parser, but the documentation here is just for use and what to expect from the parser. RealHTTP is an on going project so any bug reports, suggestions, contributions, etc are welcome.

### Functions:

**execute(data)**:

Params: data ->

**clear()**: Resets all data members of the parser to their state at time of creation. Any data still stored in the parser will be deleted, any states will be reset.


**PARTIAL(); FULL(); FAIL()**: These functions don't have too much of a purpose in python except to help the user realize the associated values are there for them.


### Data Members:

**Return Values**: FULL, PARTIAL, FAIL; these are the values that are returned to tell the status of the message that is being parsed. FULL means that one HTTP request has been completely parsed and is ready to be used. PARTIAL means that a complete message hasn't been down, but that there have been no errors so far. FAIL means that there was some error while parsing (an error message will be stored to give information on what happened). 

**content**: A string that holds the data the parser is working with or has access to. Data is stored here when there is a partial message passed into the parser and data is removed from content as it is actually parsed into the other data members.

**request_type**: The type of the HTTP request (ie GET, PUT, HEAD, etc).

**url**: The URL the HTTP is requesting.

**version**: The version the HTTP request is running on.

**headers**: A dictionary of all the request's headers. Key: name of the header   Value: body of the header

**body**: The entity body of of the HTTP request. Starts as an empty string.

**needed_body**: The number of bytes that the parser still needs to get and add to the body (the entity body). This is decremented as bytes are added to the body.

**error**: In the case that the parsing fails error is set to a string describing what happened to make the parsing fail.

**start**: Checks if the first line or the line with the request_type, URL, and version information has already been parsed. This is the result of probably not the best implementation and is a place that needs to be improved.





### Notes For Development: