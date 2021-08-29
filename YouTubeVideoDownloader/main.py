from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from pytube import YouTube
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('APP_SECRET_KEY')
Bootstrap(app)


# Main Form
class DownloadForm(FlaskForm):
    url_field = StringField("", validators=[DataRequired()], render_kw={"placeholder": "You Tube Video URL"})
    download = SubmitField("Download")


@app.route("/", methods=["GET", "POST"])
def home():
    form = DownloadForm()
    if form.validate_on_submit():
        yt_link = form.url_field.data
        try:
            # object creation using YouTube
            yt = YouTube(yt_link)
        except ConnectionError:
            flash("There was a connection error while downloading!")
            return render_template("index.html", form=form)
        stream = yt.streams.first()
        try:
            # downloading the video
            stream.download()
            flash("Download completed !")
            return render_template("index.html", form=form)
        except ConnectionError:
            flash("There was a connection error while downloading!")
            return render_template("index.html", form=form)
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
