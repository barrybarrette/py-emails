import bolt

bolt.register_task('clear-pyc', ['delete-pyc.src', 'delete-pyc.tests'])
bolt.register_task('ut', ['clear-pyc', 'nose'])
bolt.register_task('ct', ['clear-pyc', 'conttest'])
bolt.register_task('cov', ['clear-pyc', 'nose.with-coverage'])
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
    'nose': {
        'directory': './tests/unit',
        'with-coverage': {
            'options': {
                'with-coverage': True,
                'cover-erase': True,
                'cover-package': 'emails',
                'cover-html': True,
                'cover-html-dir': 'output/coverage',
            }
        }
    },
    'conttest': {
        'task': 'nose'
    }
}
