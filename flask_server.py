from flask import Flask, request, jsonify, send_file
import os
import webtooncom_scrapper
import shutil
import tempfile


app = Flask(__name__)

@app.route('/getter', methods=['POST'])
def url_getter():
    try:
        data = request.get_json()
        url = data.get('urlink') #URL = Webtoon link from client

        webtooncom_scrapper.main(url, "webtoon_images")#Dosya adi degisebilir

        #Use url as variable in app (translator_for_folder or main). 
        #Result = return of app 
        #Maindeki son imwriter yerine Image ogesini dondurup, onu isleme sokabiliriz
        #Ustteki olmasa bile imwrite ile bastirilabilir

        result = "Upload Completed, URL: " + url
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/download')
def indir_zip():
    klasor = 'tooningo/webtoon_images_translated'
    
    temp_dir = tempfile.mkdtemp()
    zip_dosya = shutil.make_archive(temp_dir + '/translated_webtoons', 'zip', klasor)
    
    return send_file(zip_dosya, as_attachment=True, download_name='translated_webtoons.zip')

if __name__ == '__main__':
    app.run(debug=True)

