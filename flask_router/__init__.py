# -*- coding: utf-8 -*-
"""
    __init__.py - extension definition
    ~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
from werkzeug.utils import import_string,find_modules

class NoRouteModuleException(Exception):
    pass

class NoRootPathSettingException(Exception):
    pass

class NoBlueprintException(Exception):
    pass

class NoInstalledBlueprintsSettingException(Exception):
    pass

class FlaskRouter(object):

    def __init__(self, app=None):
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self,app):
        if self.app is None:
            self.app = app
        self._register_blueprints = self.app.config.get('REGISTER_BLUEPRINTS')
        self._set_verbose()
        self._set_path()            
        self._register_routes()
        
    def _is_blueprint_registered(self,bp):
        return bp in self.app.blueprints.values()

    def _set_verbose(self):
        self.app.config['VERBOSE'] = (lambda: os.environ.get('VERBOSE') and True or False)()

    def _set_path(self):
        if self.app.config.get('ROOT_PATH',None) is None:
            raise NoRootPathSettingException('Must have ROOT_PATH config setting set')      
        sys.path.append(self.app.config.get('ROOT_PATH',''))    

    def _get_imported_stuff_by_path(self, path):
        module_name, object_name = path.rsplit('.', 1)
        module = import_string(module_name)
        return module, object_name
        
    def _register_routes(self):
        if self.app.config.get('VERBOSE',False):
            print 'starting routing'
        for url_module in self.app.config.get('URL_MODULES',[]):            
            module,r_name = self._get_imported_stuff_by_path(url_module)            
            if r_name == 'routes' and hasattr(module,r_name):
                if self.app.config.get('VERBOSE',False):
                    print '\tsetting up routing for {} with\n\troute module {}\n'.format(module.__package__,module.__name__)
                self._setup_routes(getattr(module,r_name))
            else:
                raise NoRouteModuleException('No {r_name} url module found'.format(r_name=r_name))
        if self.app.config.get('VERBOSE',False):
            print 'Finished registering blueprints and url routes'
            
    def _setup_routes(self,routes):
        for route in routes:
            blueprint,rules = route[0],route[1:]            
            for itm in rules:
                if len(itm) == 3:
                    pattern,endpoint,view = itm
                else:
                    pattern,view = itm
                    endpoint = None            
                if self.app.config.get('VERBOSE',False):
                    print '\t\tplugging url Pattern:{pattern}\n\t\tinto View class/function:{name}\n\t\tat endpoint:{endpoint}\n'.format(
                        pattern=pattern,
                        name=hasattr(view,'func_name') and view.view_class.__name__ or view.__name__,
                        endpoint=endpoint or view.func_name,
                    )
                if type(blueprint) == type(tuple()):
                    blueprint = blueprint[0]
                blueprint.add_url_rule(pattern,endpoint or view.func_name,view_func=hasattr(view,'func_name') and view or view.as_view(endpoint))
            if self._register_blueprints:
                if not self._is_blueprint_registered(blueprint):
                    self.app.register_blueprint(blueprint)