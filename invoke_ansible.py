import ansible
import pprint
from ansible import utils
from jinja2 import Environment, PackageLoader
from collections import namedtuple
from ansible import utils
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from callbacks import PlaybookCallback


def run_playbook(module_path=None, e_vars={}, playbook_path="site.yml", console=True):
    """ Invokes playbook """
    
    loader = DataLoader()
    variable_manager = VariableManager()
    variable_manager.extra_vars = e_vars
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=['localhost'])
    passwords = {}
    utils.VERBOSITY = 4
    Options = namedtuple('Options', ['listtags',
                                     'listtasks',
                                     'listhosts',
                                     'syntax',
                                     'connection',
                                     'module_path',
                                     'forks',
                                     'remote_user',
                                     'private_key_file',
                                     'ssh_common_args',
                                     'ssh_extra_args',
                                     'sftp_extra_args',
                                     'scp_extra_args',
                                     'become',
                                     'become_method',
                                     'become_user',
                                     'verbosity',
                                     'check'])
    options = Options(listtags=False,
                      listtasks=False,
                      listhosts=False,
                      syntax=False,
                      connection='ssh',
                      module_path=module_path,
                      forks=100,
                      remote_user='root',
                      private_key_file=None,
                      ssh_common_args=None,
                      ssh_extra_args=None,
                      sftp_extra_args=None,
                      scp_extra_args=None,
                      become=False,
                      become_method=None,
                      become_user='root',
                      verbosity=utils.VERBOSITY,
                      check=False)
    pbex = PlaybookExecutor(playbooks=[playbook_path],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)
    if not console:
        cb = PlaybookCallback()
        pbex._tqm._stdout_callback = cb
        return_code = pbex.run()
        results = cb.results
    else:
        results = pbex.run()
    return results
