from flask import Flask, session, request, render_template, redirect

import pg

db = pg.DB(dbname='chirp_db')

app = Flask('ChirpApp')

@app.route('/')
def home():
    query  = db.query('''
        select users.name, tweet_content from users inner join tweet_table on users.id = tweet_table.user_id
    ''')
    tweets = query.namedresult();
    return render_template('timeline.html', tweets = tweets)


@app.route('/tweeting', methods=['POST'])
def tweet():
    tweet = request.form['tweet']
    user_id = session['id']

    db.insert('tweet_table', tweet_content=tweet, user_id=user_id)

    return redirect('/tweeting')


@app.route('/timeline')
def timeline():
    user_id = session['id']
    timeline_query = db.query('''
        select * from tweet_table where
        tweet_table.user_id = $1 or
        tweet_table.user_id in (
            select user_id from followz where person_following = $1
        )
    order by
        time_display asc
    ''',
    user_id).namedresult()
    return render_template('timeline.html', tweets = timeline_query)





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
        return redirect('/profile/' '%s' % str(username))

        print login_validation
        if username in session:
            return render_template('profile.html',
            errormessage = True,
            title = "Login")
    else:
        return redirect('/login')




@app.route('/profile/<username>')
def profile(username):
    if username:
        query = db.query('''
    select
        users.name,
        users.username,
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

app.secret_key = 'NTOEU0948375980CTH9EO893'

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
