## Deployment model
```
+------------------------------+   +-----------------------------+
| Docker container             |   | Docker container            |
|                              |   |                             |
|   +-----------------------+  |   |  +-----------------------+  |
|   |                       +------>  | Assignment            |  |
|   |   Flask application   |  |   |  | compile, checking,    |  |
|   |                       <------+  | testing etc...        |  |
|   +----------+------------+  |   |  +-----------------------+  |
|              |               |   |                             |
|   +----------v------------+  |   +-----------------------------+
|   |                       |  |
|   | WSGI container (uWSGI)|  |
|   |                       |  |
|   +----------+------------+  |
|              |               |
|   +----------v------------+  |   +-----------------------------+
|   |                       +------>                             |
|   |   NGINX web server    |  |   |           Clients           |
|   |                       <------+                             |
|   +-----------------------+  |   +-----------------------------+
|                              |
+------------------------------+
```
### Mac OS X
Follow instructions in macosx/coreos-vagrant to setup Docker

### Deploy
Note that this is draft version and build scripts and utilities will be written
and deployment steps will be updated and simplified over time.

1. Setup Docker
2. Create 2 containers
  - One Web container
  - One for assignment management
3. Setup Web container
   - Install Python 3
   - Create virtual environment
   - Install server application requirements
   - Setup uWSGI and NGINX
   - Setup GitHub hooks for automation of deployment
4. Setup Dev container
  - Install build-essentials
  - Setup git and repositories if necessary
