import os
from flask import Flask, request, send_file, jsonify, render_template, redirect, url_for # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import tempfile
from cis_benchmark_parser import parse_cis_benchmark
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_cis_benchmark_api():
    app.logger.debug(f"Request headers: {request.headers}")
    app.logger.debug(f"Request files: {request.files}")
    app.logger.debug(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        error_message = "No file part"
        if request.accept_mimetypes.accept_json:
            return jsonify({"error": error_message}), 400
        return render_template('index.html', error=error_message)
    
    file = request.files['file']
    
    if file.filename == '':
        app.logger.error("No selected file")
        error_message = "No selected file"
        if request.accept_mimetypes.accept_json:
            return jsonify({"error": error_message}), 400
        return render_template('index.html', error=error_message)
    
    if file and file.filename.lower().endswith('.pdf'):
        app.logger.info(f"Processing file: {file.filename}")
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_filename = os.path.splitext(filename)[0] + '.csv'
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Parse the PDF
        try:
            parse_cis_benchmark(filepath, output_filepath)
            
            # Check if the output file was created and is not empty
            if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0:
                return send_file(output_filepath, as_attachment=True, download_name=output_filename)
            else:
                raise Exception("Output file is empty or was not created")
        
        except Exception as e:
            app.logger.error(f"Error processing PDF: {str(e)}")
            error_message = f"Error processing PDF: {str(e)}"
            if request.accept_mimetypes.accept_json:
                return jsonify({"error": error_message}), 500
            return render_template('index.html', error=error_message)
        
        finally:
            # Clean up files
            if os.path.exists(filepath):
                os.unlink(filepath)
            if os.path.exists(output_filepath):
                os.unlink(output_filepath)
    else:
        app.logger.error("Invalid file type")
        error_message = "Invalid file type. Please upload a PDF."
        if request.accept_mimetypes.accept_json:
            return jsonify({"error": error_message}), 400
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)