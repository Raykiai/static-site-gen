import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

# loop over all the files in the content folder
POSTS = {}
for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

#Convert the dates from string to datetime format and sort them in descending order
POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

# getting the templates
env = Environment(loader=PackageLoader('main', 'templates'))
news_template = env.get_template('news.html')
snews_template = env.get_template('snews.html')


# pass the metadata from the news page template from the POSTS list
# this will pass a list of metadata through the variable posts, to the news page template (this is the posts variable which is looped in the template)
posts_metadata = [POSTS[post].metadata for post in POSTS]
news_html = news_template.render(posts=posts_metadata)

posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
news_html = news_template.render(posts=posts_metadata, tags=tags)

# writing the html as an output to a file
with open('output/news.html', 'w') as file:
    file.write(news_html)

# rendering individual news pages
for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'summary': post_metadata['summary'],
        'title': post_metadata['title'],
        'publisher': post_metadata['publisher'],
        'date': post_metadata['date'],
        'thumbnail': post_metadata['thumbnail']
    }

    snews_html = snews_template.render(post=post_data)
    snews_file_path = 'output/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(snews_file_path), exist_ok=True)
    with open(snews_file_path, 'w') as file:
        file.write(snews_html)


# home page
with open('pages/home.md', 'r') as file:
    parsed_md = markdown(file.read(), extras=['metadata'])
    env = Environment(loader=PackageLoader('main', 'templates'))
    home_template = env.get_template('index.html')
    data = {
    'content': parsed_md,
    'title': parsed_md.metadata['title'],
    'title2': parsed_md.metadata['title2'],
    'subtitle': parsed_md.metadata['subtitle']
    }
    home_html = home_template.render(post=data)

    with open('output/index.html', 'w') as file:
     file.write(home_html)

#about page
with open('pages/about.md', 'r') as file:
    parsed_md = markdown(file.read(), extras=['metadata'])
    env = Environment(loader=PackageLoader('main', 'templates'))
    about_template = env.get_template('about.html')
    data = {
    'content': parsed_md,
    'title': parsed_md.metadata['title'],
    'member1': parsed_md.metadata['member1'],
    'member2': parsed_md.metadata['member2'],
    'member3': parsed_md.metadata['member3'],
    'position1': parsed_md.metadata['position1'],
    'position2': parsed_md.metadata['position2'],
    'position3': parsed_md.metadata['position3'],
    'thumbnail1': parsed_md.metadata['thumbnail1'],
    'thumbnail2': parsed_md.metadata['thumbnail2'],
    'thumbnail3': parsed_md.metadata['thumbnail3']
    }
    about_html = about_template.render(post=data)
    
    with open('output/about.html', 'w') as file:
     file.write(about_html)

# contact page
with open('pages/contact.md', 'r') as file:
    parsed_md = markdown(file.read(), extras=['metadata'])
    env = Environment(loader=PackageLoader('main', 'templates'))
    contact_template = env.get_template('contact.html')
    data = {
    'content': parsed_md,
    'city': parsed_md.metadata['city'],
    'country': parsed_md.metadata['country'],
    'openw': parsed_md.metadata['openw'],
    'opent': parsed_md.metadata['opent'],
    'phone': parsed_md.metadata['phone'],
    'email': parsed_md.metadata['email'],
    }
    contact_html = contact_template.render(post=data)
    
    with open('output/contact.html', 'w') as file:
     file.write(contact_html)
