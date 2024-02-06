# HTMXango

This is a demonstration of how to use htmx with Django to create a modern web application with minimal javascript.
The challenge here is to use CBVs and satisfy the need of htmx partial html rendering.

## How to run

1. Clone the repository
2. Install [Poetry](https://python-poetry.org/docs/)
3. Run `poetry install`
4. Run `poetry run python manage.py migrate`
5. Run `poetry run python manage.py runserver`

## How to use

1. Go to `http://localhost:8000/todos/`
2. Click on the buttons to see the magic happening
3. Add a new todo
4. ...

## How it works

Check the `todos/views.py` where the logic is implemented on how to respond with full or partial HTML if the request is coming from an htmx or normal request.

We rely on three major projects here:

- [htmx](https://htmx.org/) HTMX is a javascript library that allows you to access AJAX, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext.
- [django-htmx](https://github.com/adamchainz/django-htmx) A Django app to make using htmx easier.
- [django-render-block](https://github.com/clokep/django-render-block) A Django app to allow rendering of individual blocks from a template and avoid splitting templates into partials and overuse include tags. Keep in mind that include come with a cost of performance specially if you have a lot of them e.g in a loop.

Other tools like Boostrap5, crispy-forms and django are used to make the example more complete.

## Using CBVs

I'm not a big fan of function based views, so I've used class based views with small adjustments to make it work with htmx.

The CBVs can have with the help of the `HtmxTemplateResponseMixin` a `htmx_template_block` attribute that will be used to render the block of the template that will be sent back to the client if the request is originated from htmx.

The actual work of that is done in the `HtmxResponseClass` which make use of django-render-block to render the block and send it back to the client.

Check the `todos/views.py` for more details.
