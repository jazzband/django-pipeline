from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            default=False,
            help='Force update of all files, even if the source files are older than the current compressed file.'
        ),
    )
    help = 'Updates and compresses CSS and JS on-demand, without restarting Django'
    args = '<group>'

    def handle(self, group=None, **options):
        from pipeline.packager import Packager
        packager = Packager(
            sync=True,
            force=options.get('force', False),
            verbose=int(options.get('verbosity', 1)) >= 2
        )

        for package_name in packager.packages['css']:
            if group and package_name != group:
                continue
            package = packager.package_for('css', package_name)
            if packager.verbose or packager.force:
                print
                message = "CSS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_stylesheets(package)

        for package_name in packager.packages['js']:
            if group and package_name != group:
                continue
            package = packager.package_for('js', package_name)
            if packager.verbose or packager.force:
                print
                message = "JS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_javascripts(package)
