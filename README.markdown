# Codename Manana (a fork of MunkiWebAdmin)

This is an updated version of [MunkiWebAdmin from Greg Neagle](https://github.com/munki/munkiwebadmin) incorporating [patches from Steve Kueng](https://github.com/SteveKueng/munkiwebadmin/). This fork is actively maintained by the University of Oxford Mac team. Our goal was to remove the software deployment and updates entirely from the Casper Suite and facilitate a more advanced [autopkg](https://github.com/autopkg/autopkg) and [Munki](https://github.com/munki/munki) workflow.

As a result we built a Manana – a middleware to enable inventory information in the JSS to be used to manage Munki clients. Our solution integrates nicely with all tools of the Munki ecosystem: one can use autopkg, MunkiAdmin, MunkiWebAdmin, munki-staging, and all the other great Open Source software out there.

The code is in production in our environment since mid 2015. We are actively maintaining the code, but our focus is still features. So please forgive us not having spent time on a nice UI. Currently one has to rely on the code generated Django admin interface. 

Please find some set-up notes for the dynamicc manifests based on JSS inventory within the [JSS manifests application's README.md](https://github.com/ox-it/manana/blob/master/jssmanifests/README.md)

[Marko's](https://github.com/mjung/) [presentation at MacAD UK 2016](https://github.com/mjung/publications/tree/master/2016-02-09_MacAdUK) provides an overview of the workflow beginning with slide 35.
