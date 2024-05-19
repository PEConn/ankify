from genanki import Model

# NOTE: I'm not actually using this...

question_format = """
{{cloze:Text}}

<span class="tags">{{Tags}}</tags>
"""

answer_format = """
{{cloze:Text}}<br>
{{Back Extra}}

<span class="tags">{{Tags}}</tags>
"""

css = """
.card {
	font-family: arial;
	font-size: 20px;
	text-align: center;
	color: black;
	background-color: white;
}

.cloze {
	font-weight: bold;
	color: blue;
}
.nightMode .cloze {
	color: lightblue;
}

/* New stuff: */
.tags {
	font-size: 18px;
	color: lightgrey;
	position: absolute;
	bottom: 10px;
	left: 10px;
}
"""

MY_CLOZE_MODEL = Model(
		1550428389,
		'Cloze (genanki)',
		model_type=Model.CLOZE,
		fields=[
			{
				'name': 'Text',
				'font': 'Arial',
				},
			{
				'name': 'Back Extra',
				'font': 'Arial',
				},
			],
		templates=[
			{
				'name': 'Cloze',
				'qfmt': question_format,
				'afmt': answer_format,
				},
			],
		css=css,
		)

# What I want:
# 
# .footer {
#   font-size: 16px;
#   position: fixed;
#   bottom: 0px;
#   margin: auto;
#   text-align: center;
# }
# 
# 
# <div class="footer">
# {{Tags}}
# </div>
