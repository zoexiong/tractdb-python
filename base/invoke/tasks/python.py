import base.invoke.tasks.command
import base.invoke.tasks.update
import invoke
import yaml


@invoke.task(pre=[
    base.invoke.tasks.compile.compile_config,
    base.invoke.tasks.update.update_dependencies
])
def package_publish():
    # Parse our config
    with open('_base_config.yml') as f:
        config_yaml = yaml.safe_load(f)

    # Build the package
    base.invoke.tasks.command.run(
        'python setup.py sdist'
    )

    # Use wheel to publish
    # Currently using start because input for the password prompt was problematic
    base.invoke.tasks.command.run(
        'start cmd /c twine upload dist\\tractdb-{}.zip'.format(
            config_yaml['config']['package']['version']
        )
    )
