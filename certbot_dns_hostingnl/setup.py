from setuptools import setup

setup(
    name='certbot-dns-hostingnl',
    install_requires=[
        'certbot',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-hostingnl = certbot_dns_hostingnl._internal.dns_hostingnl:Authenticator',
        ],
    },
)
