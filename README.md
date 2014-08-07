# Google App Engine Server Configs

1. [Install Cloud SDK][1] and select Option 2 - Python and PHP - when prompted about App Engine.
2. Install App Engine command line interface component of Cloud SDK
by executing

  `gcloud components update app`

  Your command line tool is all set now.

3. Copy `app.yaml` file from this repo into your app build root folder:

  `curl https://raw.githubusercontent.com/h5bp/server-configs-gae/master/app.yaml > app.yaml`

4. Create a new project in [Google Developers Console][2] if you don't have one already,
and modify `application` field in the `app.yaml` to reflect your Project ID.
It is a good idea to look through the rest of `app.yaml` file in case it needs some adjustments
for your specific case.

  Also, let `gcloud` tool know what project you are using by executing:

  `gcloud config set project my-project-id`

5. You should be all set now. Any time you want to update your website,
execute the following command from the root of your app build directory:

  `gcloud preview app deploy .`



It might be a good idea to keep a master version of your `app.yaml` file and copy it over to the app root directory
as the last build step.


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
[3]: https://github.com/h5bp/server-configs-gae/graphs/contributors
