from flask import Flask, session, request, render_template, redirect

from dotenv import load_dotenv, find_dotenv
    import os

    load_dotenv(find_dotenv())

import pg

db = pg.DB(
  dbname=os.environ.get('DBNAME'),
  host=os.environ.get('DBHOST'),
  port=int(os.environ.get('DBPORT')),
  user=os.environ.get('DBUSER'),
  passwd=os.environ.get('DBPASSWORD')
)

app = Flask('ChirpApp')

@app.route('/')
def home():
    query  = db.query('''
        select users.name, tweet_content from users inner join tweet_table on users.id = tweet_table.user_id
    ''')
    tweets = query.namedresult();
    return render_template('home.html', tweets = tweets)


@app.route('/goLogin', methods = ['POST'])
def goLogin():
    return render_template('/login.html')



@app.route('/goSignup', methods = ['POST'])
def goSignup():
    return render_template('/signup.html')




@app.route('/tweeting', methods=['POST'])
def tweet():
    tweet = request.form['tweet']
    user_id = session['id']

    db.insert('tweet_table', tweet_content=tweet, user_id=user_id)

    return redirect('/tweeting')


@app.route('/timeline')
def timeline():
    username = session['username']
    timeline_query = db.query('''
        select
        tweet_table.tweet_content, tweet_table.id as tweet_id, tweet_table.hearts_amount
    from users
    left outer join
        tweet_table on users.id = tweet_table.user_id
    where users.username = '%s'
    ''' % username)
    tweets = timeline_query.namedresult();
    return render_template('timeline.html', tweets = tweets)

@app.route('/liked', methods = ['POST'])
def liked():
    user_name = session['username']
    like = request.form['liked']
    hearts_amount =request.form['hearts_amount']
    print "TWEEEEEEEEEEET",hearts_amount
    tweetID =request.form['tweetID']
    print "this is TWEETID", tweetID
#     likedStuff= db.query('''
#     select users.name, hearts,hearts_amount, users.id, tweet_table.tweet_content
# from tweet_table
# left outer join users on tweet_table.user_id = users.id where users.username = '%s'
# '''% user_name)



    print "TWEEEEEEETID",tweetID
    db.update('tweet_table',{'id': tweetID, 'hearts': True, 'hearts_amount': int(hearts_amount)+1})
    return redirect('/timeline')





@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/form_submit', methods=['POST'])
def form_submit():
    username = request.form['username']
    password = request.form['password']
    query = db.query("select * from users where users.username = $1 AND users.password =$2", username,password)
    login_validation = query.namedresult()

    if len(login_validation) > 0:
        session['username'] = username
        return redirect('/timeline')

        print login_validation
        if username in session:
            return render_template('profile.html',
            errormessage = True,
            title = "Login")
    else:
        return redirect('/login')


@app.route('/signup')
def signup():
    return render_template('signup.html')



@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    db.insert('users', name=name, email = email, username = username, password = password)

    return redirect('/')


@app.route('/profile/<username>')
def profile(username):
    if username:
        query = db.query('''
    select
        users.name,
        users.username,
        tweet_table.id as tweet_id,
        tweet_table.tweet_content,
        tweet_table.timecreated
    from users
    left outer join
        tweet_table on users.id = tweet_table.user_id
    where users.username = '%s'
''' % str(username))
    tweets = query.namedresult()


    user_info = db.query('''
        select
	       users.name,
	       users.username,
	       count(tweet_table.tweet_content) as tweet_count
        from
	       users
        inner join
	       tweet_table on users.id = tweet_table.user_id
        where
            users.username = '%s'
        group by
            users.username, users.name
    '''% username)
    tweet_counts = user_info.namedresult()

    amount_followers = db.query('''
        select
	       users.name,
	       users.username,
	       count(followz.person_following) as follower_amount
        from
	       users
        left outer join
	       followz on followz.person_following = users.id where users.username = '%s'
        group by
            users.name, users.username,followz.person_following
        ''' % username)
    follower_count = amount_followers.namedresult()

    amount_following = db.query('''
        select
	       users.name,
	       users.username,
	       count(followz.is_following_id) as following_count
        from
	       users
        left outer join
	       followz on followz.is_following_id = users.id where users.username = '%s'
        group by
            users.name, users.username,followz.is_following_id
    '''% username)
    following_count = amount_following.namedresult()
    # print "USER INFOOOOOO",user_info
    print "this is tweet counts", tweet_counts
    print "this is only tweets",tweets
    print "THIS IS AMOUNT FOLLOWERS", follower_count
    print "following count", following_count



    return render_template('profile.html', title='Profile', tweets= tweets, tweet_counts = tweet_counts, follower_count = follower_count, following_count = following_count)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


app.secret_key = 'NTOEU0948375980CTH9EO893'

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
