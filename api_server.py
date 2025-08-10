from flask import Flask, request, jsonify, send_file
from converter import convert_json_to_md_files
import io
import zipfile
import datetime

app = Flask(__name__)

@app.route('/json-to-zip', methods=['POST'])
def index():
    return "<h1>Markdown Zip Packager API is running!</h1><p>Please send a POST request to /json-to-zip with your JSON data.</p>"
def handle_zip_conversion():
    try:
        # 1. 获取输入的 JSON 数据
        input_json_data = request.get_json()
        if not input_json_data:
            return jsonify({"error": "No JSON data provided."}), 400

        # 2. 调用函数生成文件名和内容的字典
        markdown_files = convert_json_to_md_files(input_json_data)
        if "error" in markdown_files:
            return jsonify(markdown_files), 400
        
        # 3. 在内存中创建 ZIP 文件
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, content in markdown_files.items():
                # 将每个文件的内容（字符串）编码为字节，然后写入 ZIP
                zf.writestr(filename, content.encode('utf-8'))
        
        # 将文件指针移回开头，准备读取
        memory_file.seek(0)

        # 4. 生成一个动态的文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        zip_filename = f"interview_transcripts_{timestamp}.zip"
        
        # 5. 将内存中的 ZIP 文件作为附件发送给用户
        return send_file(
            memory_file,
            download_name=zip_filename,
            as_attachment=True,
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)