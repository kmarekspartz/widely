# widely
## Static Site as a Service using Amazon S3

### Usage

~~~~
mkdir www.hello-world.com
echo 'Hello world!' > www.hello-world.com/index.html
cd www.hello-world.com
widely sites:create www.hello-world.com
widely open
~~~~


### Heroku toolbelt-style command line tool

- Built using `docopt`, `prettytable`, `boto`, `feedparser`


### Issues

- Use S3's logging
- Support multipart etags (or add in our own metadata)
- Serving compressed files from S3
- Use Amazon CloudFront and Route 53
- Tests!


### MIT Licensed

- <http://www.github.com/zeckalpha/widely>


### Contact

- <mailto:kms@celador.mn>
- <http://www.celador.mn/widely>
