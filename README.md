# Google App Engine Python-backed Static Server Configs

## What is it?

Imagine a static ("single-page" AJAXy) web app that needs to talk to back end over some API.

This Google App Engine Python-based web-app configuration template gets you there:

- Content from all folders can be static. (You need to tell the file extensions you want to make static and add the folders you don't want to serve to `app.yaml` `skip_files:` section.)
- Root content is static. (`/` resolves to static `/index.html`)
- Backend API is implemented in Python and is "ghettoed" to specific "folders" under root. (i.e. `/api/`)
- No "editorial" choices (libraries) crammed down your throat. (Extend the simple, provided "Hello World" Python-based API endpoint with API implementation of your choice. Pick your own static "boilerplate")
- Google App Engine "goodies" are pre-wired. (App Stats, Warmup route, Promisses etc)
- Helper script to manage static content "rights and settings" without going nuts with copy-paste.

In August of 2013 [original HTML5Boilerplate Server Configs for Google App Engine][4] codebase was switched from Python-based to static / php-based. This repo is a second life of the original Python-based h5bp server-configs-gae spirit, but with "static first" theme.

## Getting There

1. [Install Cloud SDK][1] and select Option 2 - Python and PHP - when prompted about App Engine.
2. Install App Engine command line interface component of Cloud SDK
by executing

  `gcloud components update app`

  Your command line tool is all set now.

3. Review `app.yaml` and change what's needed. 

4. Create a new project in [Google Developers Console][2] if you don't have one already,
and modify `application` field in the `app.yaml` to reflect your Project ID.

  Also, let `gcloud` tool know what project you are using by executing:

  `gcloud config set project my-project-id`

5. You should be all set now. Any time you want to update your website,
execute the following command from the root of your app build directory:

  `gcloud preview app deploy .`


## Contributing to this project

Anyone and everyone is welcome to contribute, but please take a moment to review
the [contributing guidelines](CONTRIBUTING.md).

## Acknowledgements

Google App Engine Server Configs is only possible thanks to all the awesome
[contributors][3]!

## License

[MIT License](LICENSE.md)


[1]: https://developers.google.com/cloud/sdk/#Quick_Start
[2]: https://console.developers.google.com/
[3]: https://github.com/dvdotsenko/server-configs-gae-python/graphs/contributors
[4]: https://github.com/h5bp/server-configs-gae
