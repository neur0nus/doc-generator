from flask import Flask, request, send_file, render_template_string
import io
from docxtpl import DocxTemplate
import os

app = Flask(__name__)

# Простая HTML-форма
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Генератор резюме</title>
</head>
<body style="font-family: Arial; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2>Создайте резюме</h2>
    <form action="/generate" method="POST">
        <input type="text" name="name" placeholder="Имя" required style="width:100%; padding:8px; margin:5px 0;"><br>
        <input type="text" name="position" placeholder="Должность" required style="width:100%; padding:8px; margin:5px 0;"><br>
        <textarea name="experience" placeholder="Опыт" rows="3" style="width:100%; padding:8px; margin:5px 0;"></textarea><br>
        <textarea name="skills" placeholder="Навыки" rows="3" style="width:100%; padding:8px; margin:5px 0;"></textarea><br>
        <button type="submit" style="background:#4CAF50; color:white; padding:10px; border:none; cursor:pointer;">
            Скачать резюме
        </button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name', 'Кандидат')
    position = request.form.get('position', 'Специалист')
    experience = request.form.get('experience', 'Опыт работы')
    skills = request.form.get('skills', 'Навыки')
    
    # Создаём простой DOCX в памяти, если нет файла шаблона
    from docx import Document
    doc = Document()
    doc.add_heading('Резюме', 0)
    doc.add_paragraph(f'Имя: {name}')
    doc.add_paragraph(f'Целевая должность: {position}')
    doc.add_paragraph(f'Опыт: {experience}')
    doc.add_paragraph(f'Навыки: {skills}')
    
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    return send_file(
        file_stream,
        download_name=f'resume_{name}.docx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

