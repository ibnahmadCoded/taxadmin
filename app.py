from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", debug=True
    )  # remove when pushing to prod and change to the line below
    # app.run(debug=True)
