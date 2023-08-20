from flask import Flask, render_template, request, redirect, url_for, Response
import requests
from projects import *
from db.database_config import *
import dotenv
import os
from pathlib import Path
from googleapiclient.discovery import build


dotenv_path = Path('secrets/.env')

dotenv.load_dotenv(dotenv_path=dotenv_path)


app = Flask(__name__)

app.template_folder = 'pages'
app.static_folder = 'static'




@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('templates/index.html')

@app.route('/tools')
def tools():
    return render_template('templates/tools.html' , project_details=projects)

@app.route('/tools/yt-video-downloader' , methods=['GET'])
def yt_video_downloader():
    query=request.args.get('download')
    if query:
        download_url = f"https://www.youtube.com/watch?v={query}"
        try:
            download_url = get_video_download_url(download_url)
        except Exception as e:

            return render_template('templates/error.html' , error=f"{e}" , solution="Please ensure that the video is not set to private, is not in a live streaming state, and is available in your country.")
        return redirect(download_url)


    
    return render_template('templates/yt-video-downloader.html')

@app.route('/tools/yt-video-downloader', methods=['POST'])
def yt_video_downloader_query():
    query = request.form['query']


    if 'www.youtube.com/watch?v=' in query:
        query = query.split('www.youtube.com/watch?v=')[1]
        return redirect(url_for('yt_video_downloader' , download=query))
    

    yt_api_key = os.getenv('YOUTUBE_API_KEY')
    yt_api = build('youtube' , 'v3' , developerKey=yt_api_key)
    search_response = yt_api.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=10  # Adjust the number of results as needed
    ).execute()
    video = search_response.get('items', [])
    
    return render_template('templates/yt-video-downloader.html' , videos=video)




@app.route('/tools/stock-market-range' , methods=['GET'])
def stock_market_range():
    return render_template('templates/stock-market-range.html')




@app.route('/tools/stock-market-range' , methods=['POST'])
def stock_market_range_query():
    symbol = request.form['symbol']
    time = int(request.form['time'])
    ans = calculate_range(symbol , time)
    
    
    return render_template('templates/stock-market-range.html' , range=ans , rangepopup=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('templates/error.html' , error="404 Page not found" ,solution="Avoid visiting this page, as it does not exist.")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('templates/error.html' , error="500 Internal Server Error" , solution="You did something wrong and the server is not able to handle it or the server is down")

@app.errorhandler(403)
def forbidden(e):
    return render_template('templates/error.html' , error="403 Forbidden" , solution="You are not allowed to access this page")

@app.errorhandler(400)
def bad_request(e):
    return render_template('templates/error.html' , error="400 Bad Request" , solution="You did something wrong and the server is not able to handle it")

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('templates/error.html' , error="405 Method Not Allowed" , solution="You did something wrong and the server is not able to handle it")


if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0" , port=80)