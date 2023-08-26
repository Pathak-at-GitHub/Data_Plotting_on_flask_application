from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            data = uploaded_file.read()

            # Read the CSV data into a Pandas DataFrame
            df = pd.read_csv(io.BytesIO(data))

            column_names = df.columns.tolist()
            # Generate a plot
            plt.figure(figsize=(10, 6))
            plt.plot(df[column_names[0]], df[column_names[1]])
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('CSV Data Plot')
            plt.grid(True)

            # Save the plot to a BytesIO object
            img_stream = io.BytesIO()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)

            # Encode the plot image as base64
            plot_data = base64.b64encode(img_stream.read()).decode()

            # Render the HTML template with the plot image
            return render_template('index.html', plot_data=plot_data)

    return render_template('index.html', plot_data=None)

if __name__ == '__main__':
    app.run(debug=True)
