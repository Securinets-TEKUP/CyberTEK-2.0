from flask import Flask, request, render_template
from secrets import token_bytes
from os import system, remove
app = Flask(__name__)

@app.route('/')
def main_menu():
    return render_template('index.html')

@app.route('/submit_score', methods=['POST'])
def submit_score():
	form_data = request.form.get('score-entry')
	if not form_data:
		return render_template('index.html')

	idtag = token_bytes(4).hex()
	proto = []
	for ln in form_data.splitlines():
		mod_ln = ln.replace(' ', '') if '```' in ln else ln
		proto.append('```' if mod_ln.startswith('```{') else mod_ln)

	src_path = f"/tmp/.x_{idtag}.Rmd"
	out_path = src_path.replace(".Rmd", ".html")

	with open(src_path, "w") as handle:
		handle.write('\n'.join(proto))

	output = "Something went sideways..."
	try:
		system(f"Rscript /opt/core/rscripts/run.R {src_path}")
		with open(out_path, "r") as res:
			output = res.read()
		remove(out_path)
	except:
		pass

	remove(src_path)
	return output