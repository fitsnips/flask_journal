from flask import Flask, render_template, url_for, json
app = Flask(__name__)

#
# entries = [
#     {
#         'title': 'Always learning',
#         'date_posted': '2019-02-16 20:33:57',
#         'content': 'Always make sure your learning, if not you falling behind.'
#     },
#     {
#         'title': 'Lorem ipsum',
#         'date_posted': '2019-02-16 20:45:46',
#         'content': 'Lorem ipsum dolor sit amet, affert accumsan mentitum qui eu, ne sea choro graeci semper. Mei tation audiam ut, semper bonorum in per. Eum dicit appetere et, ut per accusata sadipscing. Mei ad saepe docendi tractatos, utamur aeterno vim cu, pri id facilisis hendrerit. Liber fabulas gubergren ad pro, cum errem quodsi in. Everti patrioque an his.'
#     },
#     {
#         'title': 'Python Coding',
#         'date_posted': '2019-02-16 21:03:21',
#         'content': 'python coding is coming along, I think in a few weeks I will be able to complete more interviews'
#     },
#     {
#         'title': 'Python for profit',
#         'date_posted': '2019-02-16 20:14:29.090902',
#         'content': 'Once we learn python the money will roll in right?',
#         'updated': '2019-02-16 20:35:43'
#     }
#  ]

def open_journal(jfile):
    # open the file, create if not present
    data = []

    try:
        with open( jfile, 'r+' ) as input:
            data = json.load( input )
    except OSError:
        print( 'Unable to open file {}'.format( jfile ) )

    return data


def write_journal(data, jfile):
    # print(json.dumps(data, sort_keys=True, indent=4, default=str ))
    try:
        with open( jfile, 'w' ) as outfile:
            json.dump( data, outfile, sort_keys=True, indent=4, default=str )
    except OSError:
        print( 'Unable to open file {}'.format( jfile ) )


journal_file = './data/journal.json'

journal_data = open_journal(journal_file)




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',entries=journal_data)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)