from mednet_app import create_app

# Create the Flask app instance using the application factory pattern
app = create_app()

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)
