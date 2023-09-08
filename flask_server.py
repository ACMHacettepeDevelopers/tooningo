from flask import Flask, request, jsonify
import os
import webtooncom_scrapper


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

        result = "Upload Completed URL: " + url
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

