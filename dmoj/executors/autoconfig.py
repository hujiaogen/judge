from collections import OrderedDict
import yaml
import yaml.representer

from dmoj.judgeenv import env
from dmoj.executors import get_available, load_executor
from dmoj.utils.ansi import ansi_style


def main():
    result = OrderedDict()
    env['runtime'] = {}

    for name in get_available():
        executor = load_executor(name)

        if executor is None or not hasattr(executor, 'Executor'):
            continue

        if hasattr(executor.Executor, 'autoconfig'):
            print ansi_style('%-43s%s' % ('Auto-configuring #ansi[%s](|underline):' % name, '')),
            try:
                config, success, feedback = executor.Executor.autoconfig()
            except (ValueError, TypeError):
                print ansi_style('#ansi[Not supported](red|bold)')
            else:
                print ansi_style(['#ansi[%s](red|bold)', '#ansi[%s](green|bold)'][success] %
                                 (feedback or ['Failed', 'Success'][success]))

                if not success and config:
                    print 'Attempted:'
                    print yaml.dump(config, default_flow_style=False).rstrip()

                if config and success:
                    result.update(config)

    yaml.add_representer(OrderedDict, yaml.representer.SafeRepresenter.represent_dict)
    print
    print ansi_style('#ansi[Configuration result](green|bold|underline):')
    print yaml.dump({'runtime': result}, default_flow_style=False).rstrip()

if __name__ == '__main__':
    main()