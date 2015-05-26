# Manana

> Munki Manifests based on JAMF Software Server settings.

Release 0.0.0.1 [Ooh-Ooh-Ooh-One] - Codename: Dwarf Cavendish

**Please note that this software is an early prototype and is not intended for production environments yet. Use it at your own risk.**

## Summary

Munki is the leading Open Source tool for software deployment on the OS X platform. The JAMF Casper Suite offers excellent features like inventory, Profile, MCX, and MDM capabilities. Manana attempts to act as glue to enable systems administrators to take advantage of both excellent tools: Munki for software deployment and the JAMF Casper Suite for everything else.

The idea is rather simple: Munki clients use dynamically generated XML for their manifests instead of the static files in the repository.

Manana generates Munki manifests based on information the JAMF Software Server (JSS). This early release of Manana uses Computer Extension Attributes to control all aspects of a Munki manifest for a given host. A user friendly web interface to edit the mappings between JSS Computer Extension Attributes and Munki manifest content is under active development.

To use Manana a Munki client has to use its UDID as ClientIdentifier and retrieve its manifest not from the manifest folder of the Munki repository but the JSS Manifests application being part of the Munki Web Admin application.


## Installation
### Summary

1. Follow the [MunkiWebAdmin installation instructions](https://github.com/munki/munkiwebadmin/wiki) to install the Manana flavour of Munki Web Admin. Please note the extra library dependencies as listed below.


2. Edit the `jssmanifests/conf.py` to configure the JSS Manifests application.
3. Ensure your Munki clients use the UDID of the system as ClientIdentifier.
4. Ensure your Munki clients retrieve their manifests via the JSS Manifests application. The generated manifests are at `<MunkiWebAdminURL>/jssmanifest/xml/<UDID>`.
   * Configure the web server to proxy requests for manifests to the JSS Manifests application.
   * Change the Munki client configuration to use a different ManifestURL.


### Additional Python library dependencies of Manana

* [python-jss](https://pypi.python.org/pypi/python-jss) [docs]()
* [PyYAML](https://pypi.python.org/???) [docs]()
* [LXML](https://pypi.python.org/???) [docs]()


### Munki repository web server configuration changes

**TODO** describe how to create an Apache2 mod_rewrite rule that filters for manifests/UDID and reverse proxies to the JSS Manifests application. 


### Client configuration changes
#### Set the Munki ClientIdentifier to the UDID of a host

Easiest is to add the following line to the script configuring your munki client. This sets the ClientIdentifier value to a host's UDID in the `/Library/Preferences/ManagedInstalls.plist` configuration file.

    defaults write /Library/Preferences/ManagedInstalls ClientIdentifier $(system_profiler SPHardwareDataType | awk '/Hardware UUID:/ { print $3 }')

However, if you are using other locations or MCX you might want to take slightly different approach.


#### Set the Munki ManifestURL 

It is recommended that you reconfigure your Munki repository web server to proxy requests for manifests to the Munki Web Admin application. Thereby the Munki Web Admin application can be isolated and only needs to be accessible by the Munki repository web server. This method does not require any client configuration changes.

If you wish not to change your Munki repository configuration you have to change the ManifestURL configuration value for all managed clients. In the following example Munki Web Admin is listening on https://munkiwebadmin.acme.com/

    defaults write /Library/Preferences/ManagedInstalls ManifestURL https://munkiwebadmin.acme.com/jssmanifest/xml/


## References

 * [Munki Preferences reference](https://github.com/munki/munki/wiki/Preferences)
 * [Munki Manifest reference](https://github.com/munki/munki/wiki/Manifests)
