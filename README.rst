============
genweb6.gpaq
============


Features
--------

Permite mostrar dashboards de Microsoft Power BI sin pedir autentificación al usuario.
​

Documentation
-------------

El paquete consiste de un controlpanel @@gpaq-settings donde almacenamos los parámetros:

- TENANT_ID
- CLIENT_ID
- CLIENT_SECRET

Este controlpanel solo es accesible para los gestores de la plataforma, los datos tendrán que ser
proporcionados por el cliente.

Despues tenemos un tipo de contenido Dashboard [ genweb6.dashboard ] con los siguientes parámetros:

- WORKSPACE_ID
- REPORT_ID

El Dashboard lo puede crear cualquier usuario editor de la plataforma.

Para todo el funcionamiento se ha adaptado la siguiente documentación / ejemplo que proporciona Microsft:

https://github.com/microsoft/PowerBI-Developer-Samples/tree/master/Python/Embed%20for%20your%20customers/AppOwnsData


Installation
------------

Install genweb6.gpaq by adding it to your buildout::

    [buildout]

    ...

    eggs =
        genweb6.gpaq


and then running ``bin/buildout``


License
-------

The project is licensed under the GPLv2.
