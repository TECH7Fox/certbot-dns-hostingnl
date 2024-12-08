from setuptools import setup, find_packages

setup(
    name='certbot-dns-hostingnl',
    url='https://github.com/TECH7Fox/certbot-dns-hostingnl',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'certbot',
    ],
    packages=find_packages(),
    entry_points={
        'certbot.plugins': [
            'dns-hostingnl = certbot_dns_hostingnl.dns_hostingnl:Authenticator',
        ],
    },
)
