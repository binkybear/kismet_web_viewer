from json import dumps
from flask import flash, render_template, session, request, Flask, Response, Markup
from json2html import *

from app.netxml_to_csv import process_net_xml

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!' # If we plan to use sessions later, change this secret key!


# Handle 404
@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404

# Sessions
def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1

# Main page
@app.route('/', methods=('GET', 'POST'))
def home():
    sumSessionCounter() # Not implemented...yet?

    return render_template('index.html')

# Check uploaded file for netxml extension
def allowed_file(filename):
    allowed_extensions = set(['netxml'])

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extensions


@app.route('/upload', methods=['POST'])
def upload():
    #netxml = request.files['file']  # Get the file

    uploaded_files = request.files.getlist("file[]")
    return_list = []

    for netxml in uploaded_files:
        if netxml and allowed_file(netxml.filename):
            netxml = netxml.read()  # Convert netxml file to string for processing
            return_list += process_net_xml(netxml)  # Returns a list of dictionaries

        elif not netxml:
            flash(u'No file uploaded. Please select a file below', 'danger')
            return render_template('index.html')
        elif not allowed_file(netxml.filename):
            flash(u'Invalid file extension. Must be a netxml file.', 'danger')
            return render_template('index.html')
        else:
            flash(u'Error processing file', 'danger')
            return render_template('index.html')

    # Add a data to JSON array...doesn't seem to work without it. Then convert to JSON
    newjson = {"data": return_list}
    newjson = dumps(newjson)

    # Convert JSON 2 HTML Table
    netxml_html = json2html.convert(json=newjson,
                                    table_attributes="cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"table table-striped table-bordered table-condensed\" id=\"main\"")  # Create HTML table

    print netxml_html

    # Hacky code to get table to play nice with datatables
    #
    netxml_html = netxml_html[410:]
    netxml_html = netxml_html[:-26]
    start_table = "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"table table-striped table-bordered table-condensed\" id=\"main\"><thead><tr><th>Cipher</th><th>DBM</th><th>ESSID</th><th>BSSID</th><th>Privacy</th><th>Authenticaton</th><th>Location</th><th>Channel</th><th>Client</th></tr></thead><tbody>"
    end_table = "</tbody></table>"

    netxml_html = start_table + netxml_html + end_table

    return render_template('upload.html', table=Markup(netxml_html))


if __name__ == '__main__':
    app.run()