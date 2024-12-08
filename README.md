certbot-dns-hostingnl
====================

[hostingnl](https://hosting.nl/) DNS Authenticator plugin for [Certbot](https://certbot.eff.org/).

This plugin automates the process of completing a `DNS-01` challenge by creating, and subsequently removing, 
`TXT` records using the hostingnl API end-points.

Installation
------------

```bash
pip install certbot-dns-hostingnl
```

Named Arguments
---------------

To start using DNS authentication for hostingnl, pass the following arguments on Certbot's command line:

Option|Description|
---|---|
`--authenticator dns-hostingnl`|Select the authenticator plugin (Required)|
`--dns-hostingnl-credentials FILE`|hostingnl credentials INI file. (Default is `/etc/letsencrypt/hostingnl.ini`)|
`--dns-hostingnl-propagation-seconds NUM`|How long to wait before veryfing the written `TXT` challenges. (Default is `120`)|

Credentials
-----------

Use of this plugin requires a configuration file containing your hostingnl API key.  
The token can be obtained from the [hostingnl API settings](https://mijn.hosting.nl/index.php?m=APIKeyGenerator) page.

An example `hostingnl.ini` file:

```ini
dns_hostingnl_api_key = <api_key>
```

The default path to this file is set to `/etc/letsencrypt/hostingnl.ini`, but this can can be changed using the
`--dns-hostingnl-credentials` command-line argument.

**CAUTION:** You should protect these API credentials as you would the password to your hostingnl account 
(e.g., by using a command like `chmod 600` to restrict access to the file).

Examples
--------

To acquire a single certificate for both `example.com` and `*.example.com`, waiting 900 seconds for DNS propagation:

    certbot certonly \
      --authenticator dns-hostingnl \
      --dns-hostingnl-credentials ~/.secrets/certbot/hostingnl.ini \
      --dns-hostingnl-propagation-seconds 900 \
      --keep-until-expiring --non-interactive --expand \
      --server https://acme-v02.api.letsencrypt.org/directory \
      -d 'example.com' \
      -d '*.example.com'
