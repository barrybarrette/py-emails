import bolt

bolt.register_task('clear-pyc', ['delete-pyc.src', 'delete-pyc.tests'])
bolt.register_task('ut', ['clear-pyc', 'set-vars.unit-test', 'shell.pytest'])
bolt.register_task('ct', ['clear-pyc', 'set-vars.unit-test', 'shell.pytest.continuous'])
bolt.register_task('cov', ['clear-pyc', 'set-vars.unit-test', 'shell.pytest.with-coverage'])
bolt.register_task('default', ['ct'])


config = {
    'delete-pyc': {
        'src': {
            'sourcedir': './emails',
            'recursive': True
        },
        'tests': {
            'sourcedir': './tests/unit',
            'recursive': True
        }
    },
    'set-vars': {
        'unit-test': {
            'vars': {
                'PYTHONPATH': '.'
            },
        },
    },
    'shell': {
        'pytest': {
            'command': 'pytest',
            'with-coverage': {
                'arguments': [
                    '--cov', 'emails',
                    '--cov-report', 'term',
                    '--cov-report', 'html:output/coverage'
                ]
            },
            'continuous': {
                'command': 'pytest-watch'
            },
        },
    },
}
