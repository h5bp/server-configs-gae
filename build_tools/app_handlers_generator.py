"""
Generates new app_dynamic_handers.yaml and app_static_handlers.yaml files
based on templates and inputs.
"""

import json
import os
import pystache
import yaml

from collections import defaultdict

DYNAMIC_HANDLERS_FILE_NAME_BASE = 'app.dynamic_handlers'
STATIC_HANDLERS_FILE_NAME_BASE = 'app.static_handlers'


class _BaseClass(object):

    handlers_file_name_base = 'overridden in subclasses'
    required_directives = []
    supported_directives = []

    @staticmethod
    def _get_current_path():
        return os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def _get_file_object(cls, filename):
        return open(
            os.path.join(cls._get_current_path(), filename),
            'rb'
        )

    @classmethod
    def _rebox_handler_source_data_to_supported_directives(cls, obj):
        new_obj = {}
        if not set(cls.required_directives).issubset(obj.keys()):
            raise Exception('Following handler data object does not contain all required keys ({}):\n{}'.format(
                cls.required_directives, obj
            ))

        for supported_directive in (cls.required_directives + cls.supported_directives):
            if supported_directive in obj:
                new_obj[supported_directive] = obj[supported_directive]

        return new_obj

    @classmethod
    def _get_handlers_source_data_iter(cls):
        with cls._get_file_object('{}.source.yaml'.format(cls.handlers_file_name_base)) as fp:
            for handler_data in yaml.load(fp)['handlers']:
                reboxed_data = cls._rebox_handler_source_data_to_supported_directives(handler_data)
                if reboxed_data:
                    yield reboxed_data


class StaticHandlersFileGenerator(_BaseClass):

    required_directives = ['extension']
    supported_directives = ['expiration', 'http_headers']
    handlers_file_name_base = STATIC_HANDLERS_FILE_NAME_BASE

    @classmethod
    def _get_template_data(cls, dynamic_prefixes=None):

        tempate_data_extensions = []

        # We unite extensions with same settings into one line in resulting .yaml
        # So here we will iterate over all extension declarations and
        # key them by hash of settings
        settings_extensions_map = defaultdict(list)

        for handler_data in cls._get_handlers_source_data_iter():
            extension = handler_data.pop('extension')
            settings = json.dumps(handler_data, sort_keys=True)
            settings_extensions_map[settings].append(extension)

        for settings, extensions in settings_extensions_map.items():
            handler_data = json.loads(settings)
            handler_data['extension'] = '|'.join([
                extension.strip('| ')
                for extension in extensions
            ])

            # mustache does not expose key name through a generic variable during iteration over hashes,
            # so for some directives we need to rebox hashes as arrays of key-value hashes
            # with defined key names.
            rebox_directives = ['http_headers']
            for rebox_directive in rebox_directives:
                if rebox_directive in handler_data:
                    handler_data[rebox_directive] = [
                        {
                            'key': key,
                            'value': value
                        }
                        for key, value in handler_data[rebox_directive].items()
                    ]

            # this helps with coditional blocks on template
            for key in handler_data.keys():
                handler_data['has_{}'.format(key)] = True

            tempate_data_extensions.append(handler_data)

        tempate_data_extensions = sorted(tempate_data_extensions, key=lambda d: d.get('expiration'))

        template_data = dict(
            extensions = tempate_data_extensions,
            dynamic_prefixes = [prefix.lstrip('/') for prefix in dynamic_prefixes], # template regex already has leading slash
            # html_expiration
            # html_custom_headers
            warning = "!!!! AUTO-GENERATED FILE !!!!"
        )

        # for index.html handlers we need to fish out expiration and headers we
        # are to serve with all .html files, if specified
        for handler_data in tempate_data_extensions:
            if 'html' in handler_data['extension']:

                expiration = handler_data.get('expiration')
                template_data['has_html_expiration'] = bool(expiration)
                template_data['html_expiration'] = expiration

                html_http_headers = handler_data.get('http_headers')
                template_data['has_html_http_headers'] = bool(html_http_headers)
                template_data['html_http_headers'] = html_http_headers

                break

        return template_data

    @classmethod
    def _generate_handlers_file_contents(cls, dynamic_prefixes=None):
        """
        :param dynamic_prefixes: List of dynamic edge path prefixes (folder names)
        :type dynamic_prefixes: list or None
        """
        template_data = cls._get_template_data(dynamic_prefixes=dynamic_prefixes)

        with cls._get_file_object('{}.yaml.mustache'.format(cls.handlers_file_name_base)) as fp:
            template = fp.read()

        return pystache.render(template, template_data)

    @classmethod
    def generate_handlers_file(cls, dynamic_prefixes=None):

        # intentionally doing it in CWD
        with open('{}.yaml'.format(cls.handlers_file_name_base), 'wb') as fp:
            fp.write(cls._generate_handlers_file_contents(dynamic_prefixes=dynamic_prefixes))


class DynamicHandlersFileGenerator(_BaseClass):

    required_directives = ['path_prefix', 'script']
    handlers_file_name_base = DYNAMIC_HANDLERS_FILE_NAME_BASE

    @classmethod
    def _generate_handlers_file_contents(cls, handlers_source_data):
        """
        :param handlers_source_data: List of handler dicts scraped from dynamic sourece yaml file
        :type handlers_source_data: list
        """
        with cls._get_file_object('{}.yaml.mustache'.format(cls.handlers_file_name_base)) as fp:
            template = fp.read()

        template_data = dict(
            handlers = handlers_source_data,
            warning = "!!!! AUTO-GENERATED FILE !!!!"
        )

        return pystache.render(template, template_data)

    @classmethod
    def generate_handlers_file(cls):

        handlers_source_data = list(cls._get_handlers_source_data_iter())
        dynamic_prefixes = [
            handler_source_data['path_prefix']
            for handler_source_data in handlers_source_data
        ]

        # intentionally doing it in CWD
        with open('{}.yaml'.format(cls.handlers_file_name_base), 'wb') as fp:
            fp.write(cls._generate_handlers_file_contents(handlers_source_data))

        return dynamic_prefixes


if __name__ == '__main__':
    dynamic_prefixes = DynamicHandlersFileGenerator.generate_handlers_file()
    StaticHandlersFileGenerator.generate_handlers_file(dynamic_prefixes=dynamic_prefixes)
