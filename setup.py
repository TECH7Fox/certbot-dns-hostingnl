from setuptools import setup, find_packages

setup(
    name='certbot-dns-hostingnl',
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
