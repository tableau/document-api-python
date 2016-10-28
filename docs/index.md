---
layout: home
---
<header class="jumbotron hero-spacer text-center">
    <h1>Document API Python</h1>
    <p>Programmatically update your Tableau workbooks and data sources.</p>
    <p>This site will get you up and running with the Python version of the Tableau Document API. The Document API, including the  samples and documentation, are all open source.</p>
    <br />
    <a class="btn btn-primary btn-lg" href="{{ site.baseurl }}/docs" role="button">Get Started</a>&nbsp;&nbsp;
    <a class="btn btn-primary btn-lg" href="https://github.com/tableau/document-api-python/archive/v0.4.0.zip" role="button">Download</a>
</header>

# Document API Overview
This repo contains Python source and example files for the Tableau Document API. We're just getting started and have plans to expand what you find here. Help us by submitting feedback, issues, and pull requests!


The Document API provides a supported way to programmatically make updates to Tableau workbook and data source files. If you've been making changes to these file types by directly updating the XML--that is, by XML hacking--this SDK is for you.


>Features include:
>
>- Support for 9.X, and 10.X workbook and data source files
>    - Including TDSX and TWBX files
>- Getting connection information from data sources and workbooks
>    - Server Name
>    - Username
>    - Database Name
>    - Authentication Type
>    - Connection Type
>- Updating connection information in workbooks and data sources
>    - Server Name
>    - Username
>    - Database Name
>- Getting Field information from data sources and workbooks
>    - Get all fields in a data source
>    - Get all fields in use by certain sheets in a workbook

We don't yet support creating files from scratch, adding extracts into workbooks or data sources, or updating field information.
