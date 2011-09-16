from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            default=False,
            help='Force compression and/or cache busting.'
        ),
        make_option('--dry-run',
            action='store_false',
            default=True,
            help='Don\'t attempt to compress package.'
        )
    )
    help = 'Updates and compresses CSS and JS on-demand'
    args = '<groups>'

    def handle(self, *args, **options):
        from pipeline.packager import Packager

        force = options.get('force', False)
        verbose = int(options.get('verbosity', 1)) >= 2
        sync = options.get('dry_run', True)

        packager = Packager(verbose=verbose)
        for package_name in packager.packages['css']:
            if args and package_name not in args:
                continue
            package = packager.package_for('css', package_name)
            if verbose:
                print
                message = "CSS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_stylesheets(package, sync=sync, force=force)

        for package_name in packager.packages['js']:
            if args and package_name not in args:
                continue
            package = packager.package_for('js', package_name)
            if verbose:
                print
                message = "JS Group '%s'" % package_name
                print message
                print len(message) * '-'
            packager.pack_javascripts(package, sync=sync, force=force)
