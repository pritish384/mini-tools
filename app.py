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
        except:
            return render_template('templates/error.html' , error="Error while downloading the video")
        return redirect(download_url)


    
    return render_template('templates/yt-video-downloader.html')

@app.route('/tools/yt-video-downloader', methods=['POST'])
def yt_video_downloader_query():
    query = request.form['query']


    if 'www.youtube.com/watch?v=' in query:
        query = query.split('www.youtube.com/watch?v=')[1]
        return redirect(url_for('yt_video_downloader' , download=query))
    

    yt_api_key = os.getenv('YOUTUBE_API_KEY')
    yt_api = build('youtube' , 'v3' , developerKey=yt_api_key ,static_discovery=False)
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

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0" , port=80)