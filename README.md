# Web-Application
(Individual Project)Web Application Project

In this Project, it contains five parts:

1. Building the foundation for the web server, the basics of HTTP and Docker.
-   setup the web server to deploy with docker.
-   Write a TCP socket server using Python and implement an HTTP server.
-   displaying content respectively based on 301 Redirect and 404 Not Found.

2. Static Site
-  Host index.html, style.css, and functions.js from the site using the server.
-  Host the utf.txt file from the site.
-  Host all of the images in the images directory of the sample site。
-  utilizing the Query String and HTML Templates features

3. More Dynamic Site.
-   storing all form submissions on the server based on the text form. 
-   Hosting All Text Form Data. convert the HTML of the home page to a template and Use the template to add all of the stored form submissions to the page.
-   Image Uploading, saving the uploaded file and storing the submitted data.
-   Display all of the images and captions uploaded. Using the template to add all of the stored images and captions to the page in any format.
-  

4. Upgrading TCP socket to Websocket
-   reading the entire frame in one read from the TCP socket (no buffering), upgrading the TCP socket to a WebSocket connection
-   parsing WebSocket frames that are received from any open WebSocket connection, parse the bits of the frame to read the payload, then sending a WebSocket frame to all connected     WebSocket clients containing the new message
-   using data structures to store the chat history and sending each message in its own WebSocket frame, Using this database to store all of the chat history for the app. 

5. Authentication
-   Use a cookie to identify and  keep track of the user status.
-   User Authntication when user logs in.
-   When a user successfully logs in, set a session token as a cookie for that user. These tokens must be stored in the database. If this cookie is set with a valid token, the       home page should display the message.
