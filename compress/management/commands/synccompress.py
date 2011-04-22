from optparse import make_option

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--force',
            action='store_true',
            default=False,
            help='Force update of all files, even if the source files are older than the current compressed file.'
        ),
    )
    help = 'Updates and compresses CSS and JS on-demand, without restarting Django'
    args = ''

    def handle_noargs(self, **options):
        from compress import packager
        packager.force = options.get('force', False)
        packager.verbose = int(options.get('verbosity', 1)) >= 2
        
        for package_name, package in packager.packages['css'].items():
            if packager.verbose or packager.force:
                print 
                message = "CSS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_stylesheets(package)

        for package_name, package in packager.packages['js'].items():
            if packager.verbose or packager.force:
                print 
                message = "JS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_javascripts(package)
