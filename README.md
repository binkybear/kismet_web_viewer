# Kismet Web Viewer

Parse a netxml file to a readable table.  Kismet web viewer uses: 

* datatables
* Bootstrap
* Flask
* json2html

## About Kismet Web Viewer

This project was meant to be run on a localhost system for a trusted user (myself).  
If you do plan on running it on the internet there should be more sanitization of the upload form.

The project relied heavily on [Meatballs1 NetXML-to-CSV](https://github.com/Meatballs1/NetXML-to-CSV
) project.  However, some code had to be changed to turn it into a JSON file.

## Screenshots

![Main Page](http://i.imgur.com/q416Z9Vh.png)

![Scan Results](http://i.imgur.com/vyfPLu1l.png)

## Requirements

* Python 2.7
* flask
* lxml
* json2html
* Web browser with Javascript enabled
* Kismet netxml file

## Installation

```bash
sudo pip install virtualenv
git clone https://github.com/binkybear/kismet_web_viewer.git
cd kismet_web_viewer
virtualenv env
. env/bin/activate
pip install --upgrade -r requirements.txt
```
To run from your virtual environment type:
```bash
python app.py
```

## Limitations
* No session saving
* No support for multi upload (yet?)
* GPS coordinates are better parsed from the [gpsxml file] (https://www.kismetwireless.net/Forum/General/Messages/1086879738.9266751).

## Liscense

Datatables and jQuery is licensed under the MIT license.

This project is free for anyone to use and modify.