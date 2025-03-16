"# url_shortener" 

### INSTALLATION

- clone the repository
- in the root folder 'url_shortener' build the docker image with: *docker compose build*
- run the app with: *docker compose run --rm url_shortener <ARGS>*

### USAGE
* To minify ad url with default expiration of 3600 seconds: *docker compose run --rm url_shortener --minify=<URL>*
  * example: *docker compose run --rm url_shortener --minify=https://www.example.com/path?q=search*

* To minify ad url with a custom expiration: *docker compose run --rm url_shortener --minify=<URL> --expiration<seconds>*
  * example: *docker compose run --rm url_shortener --minify=https://www.example.com/path?q=search --expiration=3000*

* To expand a returned short URL: *docker compose run --rm url_shortener --expand=<URL>*
  * example: *docker compose run --rm url_shortener --expand=https://myurlshortener.com/3*
  
