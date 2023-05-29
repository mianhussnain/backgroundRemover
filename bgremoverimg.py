from rembg import remove
from PIL import Image
from flask import Flask, request, send_file, jsonify
import io
import datetime
app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    # Check if an image file was submitted
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400

    image_file = request.files['image']
    
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    imageName ="upload"+timestamp_str+".png"
    print(timestamp_str)

    # Save the uploaded image file to a temporary location
    temp_path = 'tmp/'+imageName # You can change the path and file name as needed
    image_file.save(temp_path)
    
    # Load the image from the temporary file
    image = Image.open(temp_path)

    # Process the image to remove the background
    processed_image = remove(image)

    # Create a BytesIO object to save the processed image
    output_buffer = io.BytesIO()
    processed_image.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    # Clean up the temporary file
   #os.remove(temp_path)

    return send_file(output_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
