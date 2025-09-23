#!/usr/bin/env python3
"""
Enhanced Fabric deployment manager with service lifecycle management.
Improved version that handles deploy/start/stop/status operations efficiently.
"""

from fabric import Connection
import sys
import time
import argparse

class DjangoDeploymentManager:
    def __init__(self, host):
        self.host = host
        self.c = Connection(host)
        self.app_dir = '/opt/wwc/mysites/lab'
        self.venv_dir = '/opt/wwc/mysites/myvenv'
        self.log_file = '/opt/wwc/mysites/lab/django.log'

    def check_environment(self):
        """Check what components are already installed/configured"""
        status = {
            'system_packages': False,
            'venv_exists': False,
            'django_project': False,
            'nginx_configured': False,
            'django_running': False
        }

        # Check system packages
        result = self.c.run('which python3 && which nginx', warn=True)
        status['system_packages'] = result.return_code == 0

        # Check virtual environment
        result = self.c.run(f'test -d {self.venv_dir}', warn=True)
        status['venv_exists'] = result.return_code == 0

        # Check Django project
        result = self.c.run(f'test -f {self.app_dir}/manage.py', warn=True)
        status['django_project'] = result.return_code == 0

        # Check nginx configuration
        result = self.c.run('grep -q "proxy_pass.*8000" /etc/nginx/sites-enabled/default', warn=True)
        status['nginx_configured'] = result.return_code == 0

        # Check if Django is running
        result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
        status['django_running'] = result.return_code == 0

        return status

    def install_system_packages(self):
        """Install system packages only if needed"""
        print("📦 Checking system packages...")

        # Check what's missing
        missing_packages = []
        packages = ['python3', 'python3-pip', 'python3-venv', 'nginx', 'git']

        for package in packages:
            result = self.c.run(f'dpkg -l | grep -q "^ii.*{package}"', warn=True)
            if result.return_code != 0:
                missing_packages.append(package)

        if missing_packages:
            print(f"   Installing missing packages: {', '.join(missing_packages)}")
            self.c.sudo('apt update')
            self.c.sudo(f'apt install -y {" ".join(missing_packages)}')
        else:
            print("   ✅ All system packages already installed")

    def setup_environment(self):
        """Set up directory structure and virtual environment"""
        print("🏗️  Setting up environment...")

        # Create directory structure
        self.c.sudo('mkdir -p /opt/wwc/mysites')
        self.c.sudo('chown ubuntu:ubuntu /opt/wwc/mysites')

        # Check if virtual environment exists
        if not self.c.run(f'test -d {self.venv_dir}', warn=True).return_code == 0:
            print("   Creating virtual environment...")
            self.c.run(f'cd /opt/wwc/mysites && python3 -m venv myvenv')
            self.c.run(f'cd /opt/wwc/mysites && source myvenv/bin/activate && pip install django boto3')
        else:
            print("   ✅ Virtual environment already exists")
            # Ensure packages are installed
            self.c.run(f'cd /opt/wwc/mysites && source myvenv/bin/activate && pip install --quiet django boto3')

    def deploy_django_app(self, force_recreate=False):
        """Deploy Django application (idempotent)"""
        print("🚀 Deploying Django application...")

        # Check if Django project exists
        project_exists = self.c.run(f'test -f {self.app_dir}/manage.py', warn=True).return_code == 0

        if project_exists and not force_recreate:
            print("   ✅ Django project already exists, updating code only...")
            self._update_django_code()
        else:
            if project_exists:
                print("   🔄 Force recreating Django project...")
                self.c.run(f'rm -rf {self.app_dir}', warn=True)

            print("   Creating new Django project...")
            self._create_django_project()

        # Always run migrations (safe to run multiple times)
        print("   Running Django migrations...")
        self.c.run(f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py migrate')

    def _create_django_project(self):
        """Create fresh Django project with all configurations"""
        # Create Django project
        self.c.run('cd /opt/wwc/mysites && source myvenv/bin/activate && django-admin startproject lab')
        self.c.run(f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py startapp polls')

        # Create templates directory
        self.c.run(f'mkdir -p {self.app_dir}/polls/templates')

        # Deploy all configurations
        self._update_django_code()

    def _update_django_code(self):
        """Update Django code (views, templates, settings)"""
        # Update settings
        settings_content = '''from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-lab7-fabric-deployment-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['polls/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lab.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
        self.c.run(f'cat > {self.app_dir}/lab/settings.py << "EOF"\n{settings_content}\nEOF')

        # Update template
        template_content = '''<html>
<head>
    <title>Cloud Storage Files</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .file-list { background-color: #f5f5f5; padding: 20px; border-radius: 5px; }
        .file-item { background-color: white; margin: 10px 0; padding: 15px; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .file-name { font-weight: bold; color: #2c3e50; }
        .file-details { color: #7f8c8d; font-size: 0.9em; margin-top: 5px; }
        .no-files { color: #e74c3c; font-style: italic; }
        .error { color: #e74c3c; background-color: #f8d7da; padding: 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Cloud Storage Files</h1>
    <div class="file-list">
        {% if error %}
            <div class="error">{{ error }}</div>
        {% elif items %}
            <p>Found {{ items|length }} file(s) in cloud storage:</p>
            {% for item in items %}
                <div class="file-item">
                    <div class="file-name">{{ item.fileName }}</div>
                    <div class="file-details">
                        User: {{ item.userId }}<br>
                        {% if item.fileSize %}Size: {{ item.fileSize }} bytes<br>{% endif %}
                        {% if item.uploadDate %}Uploaded: {{ item.uploadDate }}{% endif %}
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p class="no-files">No files found in cloud storage.</p>
        {% endif %}
    </div>
</body>
</html>'''
        self.c.run(f'cat > {self.app_dir}/polls/templates/files.html << "EOF"\n{template_content}\nEOF')

        # Update views
        views_content = '''from django.template import loader
from django.http import HttpResponse
import boto3
from botocore.exceptions import ClientError

def index(request):
    template = loader.get_template('files.html')
    try:
        # Use default credentials (from ~/.aws/credentials or environment variables)
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        table = dynamodb.Table("UserFiles")
        response = table.scan()
        items = response.get('Items', [])
        context = {'items': items}
        return HttpResponse(template.render(context, request))
    except ClientError as e:
        error_context = {'items': [], 'error': f"Error accessing DynamoDB: {e.response['Error']['Message']}"}
        return HttpResponse(template.render(error_context, request))
    except Exception as e:
        error_context = {'items': [], 'error': f"Error: {str(e)}"}
        return HttpResponse(template.render(error_context, request))
'''
        self.c.run(f'cat > {self.app_dir}/polls/views.py << "EOF"\n{views_content}\nEOF')

        # Update URLs
        polls_urls = '''from django.urls import path
from . import views
urlpatterns = [path('', views.index, name='index')]
'''
        self.c.run(f'cat > {self.app_dir}/polls/urls.py << "EOF"\n{polls_urls}\nEOF')

        main_urls = '''from django.contrib import admin
from django.urls import include, path
urlpatterns = [path('polls/', include('polls.urls')), path('admin/', admin.site.urls)]
'''
        self.c.run(f'cat > {self.app_dir}/lab/urls.py << "EOF"\n{main_urls}\nEOF')

    def configure_nginx(self):
        """Configure nginx (idempotent)"""
        print("🌐 Configuring nginx...")

        # Check if already configured
        result = self.c.run('grep -q "proxy_pass.*8000" /etc/nginx/sites-enabled/default', warn=True)
        if result.return_code == 0:
            print("   ✅ Nginx already configured")
            return

        nginx_config = '''server {
  listen 80 default_server;
  listen [::]:80 default_server;
  location / {
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass http://127.0.0.1:8000;
  }
}'''
        self.c.run(f"echo '{nginx_config}' > /tmp/nginx_default")
        self.c.sudo('cp /tmp/nginx_default /etc/nginx/sites-enabled/default')
        self.c.sudo('systemctl restart nginx')
        print("   ✅ Nginx configured and restarted")

    def start_django(self):
        """Start Django server (only if not running)"""
        print("🚀 Starting Django server...")

        # Check if already running
        result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
        if result.return_code == 0:
            print("   ✅ Django server already running")
            return True

        # Start Django server using screen to properly detach
        start_cmd = f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py runserver 0.0.0.0:8000 > {self.log_file} 2>&1'

        # Use setsid to properly detach the process
        self.c.run(f'setsid bash -c "{start_cmd}" < /dev/null > /dev/null 2>&1 &', warn=True)

        # Wait and verify
        time.sleep(3)
        result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
        if result.return_code == 0:
            print("   ✅ Django server started successfully")
            return True
        else:
            print("   ❌ Failed to start Django server")
            return False

    def stop_django(self):
        """Stop Django server"""
        print("🛑 Stopping Django server...")

        result = self.c.run('pkill -f "manage.py runserver"', warn=True)
        if result.return_code == 0:
            print("   ✅ Django server stopped")
        else:
            print("   ℹ️  No Django server was running")

        # Wait for processes to terminate
        time.sleep(2)

    def restart_django(self):
        """Restart Django server"""
        self.stop_django()
        time.sleep(1)
        return self.start_django()

    def status(self):
        """Show deployment status"""
        print("📊 Deployment Status:")
        status = self.check_environment()

        # Format status in a clean table
        status_items = [
            ("System Packages", status['system_packages']),
            ("Virtual Environment", status['venv_exists']),
            ("Django Project", status['django_project']),
            ("Nginx Configured", status['nginx_configured']),
            ("Django Running", status['django_running'])
        ]

        for item, is_ok in status_items:
            status_icon = '✅' if is_ok else '❌'
            print(f"   {item:<20} {status_icon}")

        if status['django_running']:
            # Get hostname from SSH config
            print(f"   🌐 Access: http://{self.c.host}/polls/")

        return status

    def deploy(self, force_recreate=False):
        """Full deployment process (idempotent)"""
        print(f"🚀 Starting deployment to {self.host}...")

        try:
            self.install_system_packages()
            self.setup_environment()
            self.deploy_django_app(force_recreate)
            self.configure_nginx()

            if self.start_django():
                print(f"\n🎉 Deployment successful!")
                print(f"🌐 Access: http://{self.c.host}/polls/")
                return True
            else:
                print(f"\n❌ Deployment failed!")
                return False

        except Exception as e:
            print(f"\n❌ Deployment error: {e}")
            return False

    def logs(self, lines=50):
        """Show Django server logs"""
        print(f"📋 Django server logs (last {lines} lines):")
        result = self.c.run(f'tail -{lines} {self.log_file}', warn=True)
        if result.return_code == 0:
            print(result.stdout)
        else:
            print("   No logs found")

def main():
    parser = argparse.ArgumentParser(description='Django Deployment Manager')
    parser.add_argument('action', choices=['deploy', 'start', 'stop', 'restart', 'status', 'logs'],
                       help='Action to perform')
    parser.add_argument('--force', action='store_true',
                       help='Force recreate Django project (for deploy action)')
    parser.add_argument('--host', default='24745401-vm-lab7',
                       help='SSH host to connect to')

    args = parser.parse_args()

    manager = DjangoDeploymentManager(args.host)

    if args.action == 'deploy':
        manager.deploy(force_recreate=args.force)
    elif args.action == 'start':
        manager.start_django()
    elif args.action == 'stop':
        manager.stop_django()
    elif args.action == 'restart':
        manager.restart_django()
    elif args.action == 'status':
        manager.status()
    elif args.action == 'logs':
        manager.logs()

if __name__ == "__main__":
    main()