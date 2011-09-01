'''
The caller module is used as a front-end to manage direct calls to the salt
minion modules.
'''
# Import python modules
import os
import pprint
# Import salt libs
import salt.loader
import salt


class Caller(object):
    '''
    Object to wrap the calling of local salt modules for the salt-call command
    '''
    def __init__(self, opts):
        '''
        Pass in the command line options
        '''
        self.opts = opts
        module_dirs = [
            os.path.join(os.path.dirname(salt.__file__), 'salt/modules'),
            ] + opts['module_dirs']
        self.loader = salt.loader.Loader(module_dirs, opts)

    def call(self):
        '''
        Call the module
        '''
        return self.loader.call(self.opts['fun'], self.opts['arg'])

    def print_docs(self):
        '''
        Pick up the documentation for all of the modules and print it out.
        '''
        ret = self.loader.apply_introspection(self.loader.gen_functions())
        docs = {}
        for name in ret:
            if not docs.has_key(name):
                if ret[name].__doc__:
                    docs[name] = ret[name].__doc__
        for name in sorted(docs):
            if name.startswith(self.opts['fun']):
                print name + ':'
                print docs[name]
                print ''

    def print_grains(self):
        '''
        Print out the grains
        '''
        grains = salt.loader.grains(self.opts)
        pprint.pprint(grains)

    def run(self):
        '''
        Execute the salt call logic
        '''
        if self.opts['doc']:
            self.print_docs()
        elif self.opts['grains_run']:
            self.print_grains()
        else:
            print self.call()


