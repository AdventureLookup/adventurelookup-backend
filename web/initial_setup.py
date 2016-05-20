#!/usr/bin/env python

# Sets up the initial superuser
# Run using "docker-compose run -d web python initial_setup.py"
import django
django.setup()

from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@adventurelookup.com', 'admin')
