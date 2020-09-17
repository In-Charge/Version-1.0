from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

host_engine = create_engine('sqlite:///host.db')


class FetchedData(db.Model):
    # __bind_key__ = 'fetched'
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_fetched = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Entry %r>' % self.id


@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    if request.method == 'POST':
        id = request.form['id']
        access_token = request.form['access_token']
        query = host_engine.execute(
            # 'SELECT id, content FROM host_data')
            f'SELECT id, content FROM host_data WHERE id={id} AND access_token=\'{access_token}\'')
        print(query)
        # print(query.fetchall())
        result = query.fetchone()
        print(result)
        wrong = result is None

        if wrong:
            print('yoo')
            return render_template('fetch.html', wrong=True)
        else:
            content = result[1]
            new_item = FetchedData(host_id=id, content=content)
            db.session.add(new_item)
            db.session.commit()
            return render_template('fetch.html', wrong=False)
    else:
        return render_template('fetch.html', wrong=False)


if __name__ == '__main__':
    app.run()
