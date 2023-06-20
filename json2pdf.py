import sys
import json
from PDFWriter import PDFWriter

def error_exit(message):
    sys.stderr.write(message)
    sys.exit(1)

def JSONtoPDF(json_data):
    # Get the data values from the JSON string json_data.
    try:
        data = json.loads(json_data)
        pdf_filename = data['pdf_filename']
        font_name = data['font_name']
        font_size = data['font_size']
        header = data['header']
        footer = data['footer']
        lines = data['lines']
    except Exception as e:
        error_exit("Invalid JSON data: {}".format(e.message))
    # Generate the PDF using the data values.
    try:
        with PDFWriter(pdf_filename) as pw:
            pw.setFont(font_name, font_size)
            pw.setHeader(header)
            pw.setFooter(footer)
            for line in lines:
                pw.writeLine(line)
    except IOError as ioe:
        error_exit("IOError while generating PDF file: {}".format(ioe.message))
    except Exception as e:
        error_exit("Error while generating PDF file: {}".format(e.message))
    r