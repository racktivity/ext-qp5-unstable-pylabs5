__author__ = 'aserver'
__tags__   = 'configure',

import os

# TODO - MNour: Change when SAL(s) are implemented
def _stop_swift():
    try:
        q.system.process.run('swift-init all stop')
    except SystemExit as sys_exit_excp:
        if sys_exit_excp.code != 44:
            raise

# TODO - MNour: Change when SAL(s) are implemented
def _start_swift():
    q.system.process.run('swift-init all start')

def main(q, i, params, tags):
    qpackage = params['qpackage']
    proxy_server_conf_path = q.system.fs.joinPaths(os.path.sep, 'etc', 'swift', 'proxy-server.conf')
    pipeline_main_section_name = 'pipeline:main'
    pipeline_key_name = 'pipeline'

    _stop_swift()
    if not q.system.fs.exists(proxy_server_conf_path):
        raise Exception('Can not find file: %s' % proxy_server_conf_path)

    proxy_server_conf = q.tools.inifile.open(proxy_server_conf_path)
    if not pipeline_main_section_name in proxy_server_conf.getSections():
        raise Exception('Can not find section [%s] in file %s. Maybe it is corrupted!' % (pipeline_main_section_name, proxy_server_conf_path))

    pipeline_main_section = proxy_server_conf.getSectionAsDict(pipeline_main_section_name)
    if not pipeline_key_name in pipeline_main_section:
        raise Exception('Can not find key %s under section [%s] in file %s. Maybe it is corrupted.' % (pipeline_key_name, pipeline_main_section_name, proxy_server_conf_path))

    pipeline_value = pipeline_main_section.get(pipeline_key_name)
    if 'tempauth' in pipeline_value:
        pipeline_value = pipeline_value.replace('tempauth', 'pssd', 1)
    elif 'swauth' in pipeline_value:
        pipeline_value = pipeline_value.replace('swauth', 'pssd', 1)
    else:
        splits = pipeline_value.rsplit(' ', 1)
        pipeline_value = '%s pssd %s' % (splits[0].strip(), splits[-1].strip())

    proxy_server_conf.setParam(pipeline_main_section_name, pipeline_key_name, pipeline_value)
    proxy_server_conf.write()
    _start_swift()

