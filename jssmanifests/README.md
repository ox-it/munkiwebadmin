# Manana

> Munki Manifests based on JAMF Software Server settings.

Release 0.0.0.1 [Ooh-Ooh-Ooh-One] - Codename: Dwarf Cavendish

**Please note that this software is an early prototype and is not intended for production environments yet. The developers use it internally for production, but we have to warn you that you should understand the code before even considering doing so, too. Use it at your own risk.**

## Summary

Munki is the leading Open Source tool for software deployment on the OS X platform. The JAMF Casper Suite offers excellent features like inventory, Profile, MCX, and MDM capabilities. Manana attempts to act as glue to enable systems administrators to take advantage of both excellent tools: Munki for software deployment and the JAMF Casper Suite for everything else.

The idea is rather simple: Munki clients use dynamically generated XML for their manifests instead of the static files in the repository.

Manana generates Munki manifests based on information the JAMF Software Server (JSS). This early release of Manana uses Computer Extension Attributes to control all aspects of a Munki manifest for a given host. A user friendly web interface to edit the mappings between JSS Computer Extension Attributes and Munki manifest content is under active development.

A Munki client has to use its UDID as ClientIdentifier and retrieve its manifest from Manana's JSS Manifests application. 


## Installation
### Summary

1. Follow the [MunkiWebAdmin installation instructions](https://github.com/munki/munkiwebadmin/wiki) to install the Manana flavour of Munki Web Admin. Please note the extra library dependencies as listed below.
2. Create your MunkiWebAdmin configuration based on the `munkiwebadmin/settings_template.py` which also configures the JSS Manifests application. 
3. Ensure your Munki clients use the UDID of the system as ClientIdentifier.
4. Ensure your Munki clients retrieve their manifests via the JSS Manifests application. The generated manifests are at `<MananaURL>/jssmanifest/xml/<UDID>`.
   * Configure the web server to proxy requests for manifests to Manana's JSS Manifests application.
   * Change the Munki client configuration to use a different ManifestURL.


### Additional Python library dependencies of Manana

* [python-jss](https://pypi.python.org/pypi/python-jss) [docs]()
* [PyYAML](https://pypi.python.org/???) [docs]()
* [LXML](https://pypi.python.org/???) [docs]()



### Configuration changes
#### Set the Munki ClientIdentifier to the UDID of a host

Easiest is to add the following line to the script configuring your munki client. This sets the ClientIdentifier value to a host's UDID in the `/Library/Preferences/ManagedInstalls.plist` configuration file.

    defaults write /Library/Preferences/ManagedInstalls ClientIdentifier $(system_profiler SPHardwareDataType | awk '/Hardware UUID:/ { print $3 }')

However, if you are using other locations or MCX you might want to take slightly different approach.

#### Ensure Munki uses the dynamic manifests

Munki needs to be configured to download the manifests (at least the computer UDID based ones) from Manana. This can be achieved several ways, the two easiest ones might be:
 1. Change the Munki Preference `ManifestURL` to download all manifests from Manana (supported),
 1. Change the web server configuration serving your Munki repository to proxy all requests for Manifests (or just the UDID ones) to Manana

##### Option 1: set the Munki ManifestURL 

It is recommended that you reconfigure your Munki repository web server to proxy requests for manifests to the Munki Web Admin application. Thereby the Munki Web Admin application can be isolated and only needs to be accessible by the Munki repository web server. This method does not require any client configuration changes.

If you wish not to change your Munki repository configuration you have to change the ManifestURL configuration value for all managed clients. In the following example Manana (aka Munki Web Admin) is listening on https://manana.acme.com/

    defaults write /Library/Preferences/ManagedInstalls ManifestURL https://manana.acme.com/jssmanifest/xml/

##### Option 2: proxy via the Munki repository web server

One might want to avoid changing the client configuration for the ManifestURL. Our recommneded implementation to use the dynamic manifests is to configure the web server hosting the munki repository to proxy the manifests (preferably just the UDID based ones) to Manana. In the following example Manana (aka Munki Web Admin) is listening on https://manana.acme.com/. To enable reverse proxy for all Manifests using Apache2 one might want to use something like the following configuration snippet:

    RewriteEngine On 
    SSLProxyEngine On
    RewriteRule ^/production/manifests/(.*) https://manana.acme.com/jssmanifests/xml/$1 [P]`


## References

 * [Munki Preferences reference](https://github.com/munki/munki/wiki/Preferences)
 * [Munki Manifest reference](https://github.com/munki/munki/wiki/Manifests)
