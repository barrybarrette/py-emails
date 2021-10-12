import bolt

bolt.register_task('clear-pyc', ['delete-pyc.src', 'delete-pyc.tests'])
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['clear-pyc', 'shell.pytest.continuous'])
bolt.register_task('cov', ['clear-pyc', 'shell.pytest.with-coverage'])
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
