from library import app

# checks if file has executed directly and not imported
if __name__ == "__main__":
    app.run(debug=True)