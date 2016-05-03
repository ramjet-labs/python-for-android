from pythonforandroid.recipe import CompiledComponentsPythonRecipe, CythonRecipe
from os.path import join


class NetifacesRecipe(CythonRecipe):
    name = 'netifaces'
    version = '0.10.4'
    url = 'https://pypi.python.org/packages/source/n/netifaces/netifaces-{version}.tar.gz'
    site_packages_name = 'netifaces'
    depends = [] # [('python2', 'python3crystax')] and []#, 'setuptools']

    def __init__(self, *args, **kwargs):
        super(NetifacesRecipe, self).__init__(*args, **kwargs)
        self.depends = [('python3crystax')]

    def get_recipe_env(self, arch=None):
        env = super(NetifacesRecipe, self).get_recipe_env(arch)

        # TODO: fix hardcoded path
        # This is required to prevent issue with _io.so import.
        hostpython = self.get_recipe('hostpython2', self.ctx)
        if 'hostpython2' in self.ctx.recipe_build_order:
            env['PYTHONPATH'] = (
                join(hostpython.get_build_dir(arch.arch), 'build',
                     'lib.linux-x86_64-2.7') + ':' + env.get('PYTHONPATH', '')
            )
        return env

    def extra_build_ext_args(self, arch):
        ldflags = self.get_recipe_env(arch).get('LDFLAGS')
        flags_to_return = []
        search_paths = []
        for flag in ldflags.split(" "):
            if flag.startswith("-L"):
                search_paths.append(flag[len("-L"):].strip())
            elif flag.strip():
                flags_to_return.append(flag.strip())
        if search_paths:
            flags_to_return.insert(0, "-L%s" % ":".join(search_paths))
        flags_to_return.append("-lpython3.5m")
        return flags_to_return


recipe = NetifacesRecipe()
