from django.core.management.base import BaseCommand
from optparse import make_option

from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force', action='store_true', default=False, help='Force update of all files, even if the source files are older than the current compressed file.'),
        make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    help = 'Updates and compresses CSS and JavsScript on-demand, with no need to restart Django'
    args = ''

    def handle(self, **options):
        
        force = options.get('force', False)
        verbosity = int(options.get('verbosity', 1))

        from compress.utils import needs_update, filter_css, filter_js

        for name, css in settings.COMPRESS_CSS.items():
            if force or needs_update(css['output_filename'], css['source_filenames']):

                if verbosity >= 1:
                    print ("Updating CSS group %s..." % name),

                filter_css(css, verbose=(verbosity >= 2))

                if verbosity >= 1:
                    print "done."

        for name, js in settings.COMPRESS_JS.items():
            if force or needs_update(js['output_filename'], js['source_filenames']):

                if verbosity >= 1:
                    print ("Updating JavaScript group %s..." % name),

                filter_js(js, verbose=(verbosity >= 2))

                if verbosity >= 1:
                    print "done."