from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

PASSWORD = "sami4321"

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Website Analysis Tool</title>
</head>
<body>
    {% if not authorized %}
        <form method="POST">
            <label>Password:</label>
            <input type="password" name="password" required>
            <input type="submit" value="Login">
        </form>
    {% else %}
        <h2>Website Analysis Tool</h2>
        <form method="POST">
            <label>Enter Website URLs (one per line):</label><br>
            <textarea name="urls" rows="10" cols="50"></textarea><br>
            <label>Select Data Providers:</label><br>
            <input type="checkbox" name="ahrefs" checked> Ahrefs (Traffic & DR)<br>
            <input type="checkbox" name="seo_checker" checked> WebsiteSEOChecker (DA & Spam Score)<br>
            <input type="submit" value="Analyze">
        </form>

        {% if results %}
            <h3>Results:</h3>
            <pre>{{ results }}</pre>
        {% endif %}
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'password' in request.form:
        if request.form['password'] == PASSWORD:
            return render_template_string(HTML_FORM, authorized=True)
        else:
            return "Wrong password."
    elif request.method == 'POST' and 'urls' in request.form:
        urls = request.form['urls'].splitlines()
        use_ahrefs = 'ahrefs' in request.form
        use_seo = 'seo_checker' in request.form

        results = analyze_websites(urls, use_ahrefs, use_seo)
        return render_template_string(HTML_FORM, authorized=True, results=results)

    return render_template_string(HTML_FORM, authorized=False)

def analyze_websites(urls, use_ahrefs, use_seo):
    output = ""
    for url in urls:
        output += f"\nWebsite: {url}"
        if use_ahrefs:
            output += "\n- DR: [Ahrefs DR Here]"
            output += "\n- Traffic: [Ahrefs Traffic Here]"
        if use_seo:
            output += "\n- DA: [SEOChecker DA Here]"
            output += "\n- Spam Score: [SEOChecker Score Here]"
        output += "\n- Niche: [Auto-detected Niche]"
        output += "\n- Email: [Detected Email]"
        output += "\n- Category: [Detected Category]"
        output += "\n- Blog: Yes/No"
        output += "\n-------------------------"
    return output

if __name__ == '__main__':
    app.run(debug=True)
