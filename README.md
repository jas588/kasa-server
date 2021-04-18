<h1 align="center">Kasa Server 🖥💡🔌</h1>

Kasa Server was developed to create a client agnostic lightweight approach to controlling your TP-Link Kasa smart home devices.

Built in Python using Flask this RESTful server application wraps the [Python Kasa](https://github.com/python-kasa/python-kasa) library and allows you to control your [TP-Link Kasa](https://www.kasasmart.com) smart home devices through web based endpoints.


## Installation 🔧
The application is tested on **Python 3.9**

Get started by cloning the repository:
```
$ git clone https://github.com/jas588/kasa-server
```

I reccommend creating a virtual environment. You can create one and activate it by:
```
$ python3.9 -m venv .venv
$ source .venv/bin/activate
```

Install the required packages:
```
$ pip install -r requirements.txt
```


## Starting the server 🏁
### Using the default configuration
Launching the application on your computer is simple. Since we've named the Flask application `app.py` we don't need to specify anything more like an environment variable so you can run the project from within the project directory with the command:
```
$ flask run
```

### Custom configuration
If you want to change the name of `app.py` to something else like `server.py` you can do so just as long you run
```
$ export FLASK_APP=server.py
```
and then you can run the application as normal with
```
$ flask run
```

Alternatively you can also substitute `flask run` for `python3.9 -m flask run`


To run the server and connect to it from other devices on your local network you'll need to specify the `host` flag as such:
```
$ flask run --host=0.0.0.0
```

For more help, support and documentation about Flask please see their helpful guide [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/).

### Running the application without starting the Flask server
You can always choose to run the application without starting the Flask server since the business logic is seperate from the server logic. See `main.py` for examples on directing calling the logic. You can edit it and then run it simply with:
```
$ python3.9 main.py
```


## Example usage 🕹
You can access the server by using the base url `http://127.0.0.1:5000` or `http://localhost:5000` on your computer or by substituting for the local IP address of the computer running the application on your network, in which case remember to specify the `host` flag. The examples below will just be using localhost. 

### Get all devices
**Request**
```http
GET /devices HTTP/1.1
Host: 127.0.0.1:5000
```

**Response**
```json
{
  "count": 2,
  "_links": {
    "self": {
      "href": "/devices"
    }
  },
  "_embedded": {
    "devices": [
      {
        "name": "Family Room Light",
        "ip_address": "192.168.1.9",
        "is_on": false,
        "_links": {
          "self": {
            "href": "/devices/Family%20Room%20Light"
          },
          "toggle": {
            "href": "/devices/Family%20Room%20Light/toggle"
          },
          "on": {
            "href": "/devices/Family%20Room%20Light/on"
          },
          "off": {
            "href": "/devices/Family%20Room%20Light/off"
          }
        }
      },
      {
        "name": "Living Room Plug",
        "ip_address": "192.168.1.10",
        "is_on": true,
        "_links": {
          "self": {
            "href": "/devices/Living%20Room%20Plug"
          },
          "toggle": {
            "href": "/devices/Living%20Room%20Plug/toggle"
          },
          "on": {
            "href": "/devices/Living%20Room%20Plug/on"
          },
          "off": {
            "href": "/devices/Living%20Room%20Plug/off"
          }
        }
      }
    ]
  }
}
```

### Toggle a device
**Request**
```http
PUT /devices/Family%20Room%20Light/toggle HTTP/1.1
Host: 127.0.0.1:5000
```

**Response**
```http
204 NO CONTENT
```


## License
This project uses the [MIT License](LICENSE.txt)