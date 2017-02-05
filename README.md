# RealHTTP - An HTTP parser

While there are other parsers, I created RealHTTP because I've been really dissatisfied with what's out there, particularly with poorly named functions and lack of documentation. With RealHTTP I'm hoping it's a parser that is intuitive to use and one with easy to read documentation (found below). There are some comments in the code to help explain the use and implementation of the parser, but the documentation here is just for use and what to expect from the parser. RealHTTP is an on going project so any bug reports, suggestions, contributions, etc are welcome.  
**Note:** While I want this parser to be intuitive to use neither the documentation here nor the comments in the code are meant to teach someone how to use HTTP; it's only purpose is to teach someone how to use RealHTTP to parse HTTP messages.  

### Functions:

**execute(data)**    
**data**: the string representing the HTTP message.  
This function is where the actual parsing takes place. Once data is passed in the parser will check to see if a complete HTTP message is contained in the string. If there is a complete message it will be split into the method, resource or path, HTTP version, then the headers, and finally return FULL (note that the body of the message is NOT parsed). If the message does not contain a complete message no parsing will take place and all the data will be stored in "content" which can be accessed by the get_remainder() function. If for whatever reason the parsing fails, FAIL will be returned and an error message will be assigned to "error," which can be accessed with get_error().  
**IMPORTANT:** The parser will only go through one message at a time, even if there are multiple complete messages in "data"; FULL will be returned when the first message has been parsed. The user must be sure to use get_remainder() as to not lose any information.

**execute_body(data)**  
**data**: the string representing the remaining body of the HTTP message.  
There are two ways of telling if this function needs to be run: 1) call get_needed_body() which tells how many bytes the entity body still needs to be complete, or 2) access the headers with get_headers() and look at the "content-length" entry. If a body does need to be parsed the user passes in any remaining data for extract the needed bytes. If the message is completely parse FULL will be returned. If the body needs more PARTIAL will be returned. Theoretically FAIL maybe returned, but this functionality is not currently implemented.  
**IMPORTANT:** This function will only be successful if called after execute(); it is the user's responsibility (at least for now) to make sure that there is no body that needs to be parsed before moving on to the next message.  

**get_needed_body()**  
Returns the number of bytes that still need to be parsed to complete the entity body. Will return 0 if no more bytes are needed or if there is no entity body to parse.  

**get_headers()**  
Returns a dictionary (or map) or headers: key = header name, value = header content. Will return None if no headers have been parsed.  

**get_body()**  
Returns the entity body of the message, if there is one. Returns None if there is not body or if the body has not been completely parsed (ie, get_body() has not returned FULL).  

**get_remainder()**  
Returns any remaining data after parsing a string that has been passed into execute() or execute_body(). If execute() returns PARTIAL or FULL all data that was passed into it will be stored and can be accessed using get_remainder(); if execute() returns FULL only the data not included in the first part of the HTTP message (not including any entity body) will be stored and can be accessed by get_remainder().  
If execute_body() returns PARTIAL there will be no data stored and get_remainder will only return an empty string; it execute_body() returns FULL any remaining data (if there is any) will be stored and can be accessed with get_remainder().  
**Development Note:** It is a good idea to use get_remainder() after execute() or execute_body() returns FULL and cache the data. While in the middle of parsing (ie, before FULL is returned) the two functions just mentioned will concatenate the data you pass in with what data is already stored. However, if you go out of scope, say after you have parsed a single message, any data stored in the parser will be lost. A developer can choose to use the RealHTTP parser as a cache, but the details of making that work is up to them.  

**get_error()**  
Returns the error string. This will only be set if execute() or execute_body() returns FAIL; the string will describe the problem as best as it can.  

**get_method_type()**  
Returns the method the HTTP request is sending (eg, GET, POST, HEAD, etc). Will return None if the method has not been parsed.  

**get_url()**  
Though a slight misnomer for anyone who wants to be really technical, this returns the url present in the HTTP request (also known as the resource or path). Will return None if the url has not been parsed.  

**get_version()**  
Returns the version of HTTP that the request specified. Will return None if the version has not been parsed.  

**clear()**  
Resets all data members of the parser to their state at time of creation. Any data still stored in the parser will be deleted, any states will be reset.

**PARTIAL(); FULL(); FAIL()**  
These functions don't have too much of a purpose in python except to help the user realize the associated values are there for them.  

**test(request)**
**request:** A string representing a HTTP message.  
A simple function for testing, not really useful in actually using the parser, but more for developing the parser. Takes in a request message, calls execute, prints out relevant data members, tries to parse the entity body and prints out the body if there is one.  

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
**get_remainder():** It is a good idea to use get_remainder() after execute() or execute_body() return FULL and cache the data. While in the middle of parsing (ie, before FULL is returned) the two functions just mentioned will concatenate the data you pass in with what data is already stored. However, if you go out of scope, say after you have parsed a single message, any data stored in the parser will be lost. A developer can choose to use the RealHTTP parser as a cache, but the details of making that work is up to them.