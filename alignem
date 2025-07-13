#!/usr/bin/env python3

print('AlignEM:')
import os, sys, inspect

# if not getpass.getuser() in ('joelyancey', 'joely', 'jyancey', 'tmbartol', 'tbartol', 'bartol', 'ama8447', 'aalario'):
#     sys.exit()

hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)

print(f'\nEnvironment activated successfully. alignEM will launch shortly...\n')
print(f'Python executable: {sys.executable}')

import os

import qtpy
dirname = os.path.dirname(qtpy.__file__)

plugin_path = os.path.join(dirname,'plugins','platforms')
print(f'Qt plugin path: {plugin_path}')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

import subprocess as sp
import logging, argparse
import faulthandler
from qtpy import QtCore
from qtpy.QtCore import QCoreApplication, Qt
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QApplication

# import tensorstore as ts
from src.ui.main_window import MainWindow
from src.utils.helpers import check_for_binaries, initialize_user_preferences, \
    is_tacc, is_joel, is_mac, print_exception, register_login, convert_projects_model, addLoggingLevel, \
    check_macos_isdark_theme

import src.config as cfg

global app

class CustomFormatter(logging.Formatter):
    # ANSI color codess
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    purp = "\x1b[38;5;25m"
    blue = "\x1b[1;34m"
    debug_blue = '\x1b[38;5;57m'
    cyan = "\x1b[36m"
    # blue = "\x1b[44m"
    reset = "\x1b[0m"
    format = '%(asctime)s %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
    format2 = '%(asctime)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
    FORMATS = {
        # logging.DEBUG: grey + format + reset,
        logging.DEBUG: red + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: bold_red + format + reset,
        # logging.CRITICAL: bold_red + format2 + reset,
        # logging.CRITICAL: cyan + format2 + reset,
        logging.CRITICAL: purp + format2 + reset,
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


def main():

    # logger = logging.getLogger() # reference to root logger
    logger = logging.getLogger('root') # reference to root logger
    if is_joel():
        # logger.setLevel(logging.DEBUG)
        logging.root.setLevel(logging.DEBUG)
    else:
        # logger.setLevel(logging.INFO)
        logging.root.setLevel(logging.INFO)

    logger.info('')
    # logger = logging.getLogger(__name__)
    # logging.propagate = False  # stops message propogation to the root handler
    # fh = logging.FileHandler('messages.log')
    # logger.addHandler(fh)
    # logger.info('Running ' + __file__ + '.__main__()')
    # logger.critical('start cwd: %level' % os.getcwd())
    # logger.critical('directory of this script: %level' % os.file_path.dirname(__file__))
    # # os.chdir(os.file_path.dirname(__file__))
    # logger.critical('new cwd: %level' % os.getcwd())

    # logger.info('Setting Qt.AA_ShareOpenGLContexts')
    # QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts) #1015-
    # QCoreApplication.setAttribute(Qt.AA_UseOpenGLES) #1015-
    QCoreApplication.setApplicationName("alignEM")

    addLoggingLevel('VERSIONCHECK', logging.DEBUG + 5)
    logging.getLogger('init').setLevel("VERSIONCHECK")
    logging.getLogger('init').versioncheck('alignEM               : %s' % cfg.VERSION)
    logging.getLogger('init').versioncheck('environment           : %s' % sys.version)
    logging.getLogger('init').versioncheck('QtCore.__version__    : %s' % QtCore.__version__)
    # logging.getLogger('init').versioncheck('qtpy.PYQT_VERSION     : %s' % qtpy.PYQT_VERSION)
    # logging.getLogger('init').versioncheck('qtpy.PYSIDE_VERSION   : %s' % qtpy.PYSIDE_VERSION)
    # logging.getLogger('init').versioncheck('Jupyter QtConsole     : %s' % qcv)

    logger.debug('\n\nIf this message is seen then the logging level is set to logging.DEBUG\n')

    check_for_binaries()

    parser = argparse.ArgumentParser()
    # parser.add_argument('--api', default='pyqt5', help='Python-Qt API (pyqt6|pyqt5|pyside6|pyside2)')
    parser.add_argument('--debug', action='store_true', help='Debug Mode')
    parser.add_argument('--debug_mp', action='store_true', help='Set python multiprocessing debug level to DEBUG')
    parser.add_argument('--loglevel', type=int, default=1, help='Logging Level (0-4)')
    # parser.add_argument('--no_tensorstore', action='store_true', help='Does not use Tensorstore if True')
    parser.add_argument('--headless', action='store_true', help='Do not embed the neuroglancer browser if True')
    parser.add_argument('--no_splash', action='store_true', help='Do not start up with a splash screen')
    parser.add_argument('--dummy', action='store_true', help='Start the application using a dummy project')
    parser.add_argument('--profile', action='store_true', help='Profile performance of memory and multiprocessing')
    args = parser.parse_args()

    # os.environ["PYTHONWARNINGS"] = 'ignore'
    logging.getLogger('asyncio').disabled = True
    logging.getLogger('tornado.access').disabled = True

    if logger.hasHandlers():  logger.handlers.clear() #orig
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    LOGLEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(LOGLEVELS[args.loglevel])
    if args.debug_mp:
        cfg.DEBUG_MP = 1
    # if args.no_tensorstore: cfg.USE_TENSORSTORE = False
    if args.headless:  cfg.HEADLESS = True
    if args.no_splash: cfg.NO_SPLASH = True
    if args.profile:
        cfg.PROFILING_MODE = True


    if is_tacc():
        try:
            register_login()
        except:
            print_exception()
        try:
            bashrc = os.path.join(os.getenv('HOME'), '.bashrc')

            try:
                appendme = """\nalias alignem='source $WORK/swift-ir/tacc_bootstrap'"""
                check_str = """alias alignem="""
                with open(bashrc, "r") as f:
                    found = any(check_str in x for x in f)
                logger.info(f"Quick launch alias 'alignem' found? {found}")
                if not found:
                    logger.critical("Adding quick launch alias 'alignem'...")
                    with open(bashrc, "a+") as f:
                        f.write(appendme)
                    logger.info("Sourcing bashrc...")
                    sp.call(['source', '$HOME/.bashrc'])
            except:
                print_exception()

            try:
                appendme = """\nalias alignemdev='source $WORK/swift-ir/tacc_develop'"""
                check_str = """alias alignemdev="""
                with open(bashrc, "r") as f:
                    found = any(check_str in x for x in f)
                logger.info(f"Quick launch alias 'alignemdev' found? {found}")
                if not found:
                    logger.critical("Adding quick launch alias 'alignemdev'...")
                    with open(bashrc, "a+") as f:
                        f.write(appendme)
                    logger.info("Sourcing bashrc...")
                    sp.call(['source', '$HOME/.bashrc'])
            except:
                print_exception()
        except:
            print_exception()


    # https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html
    # Forces the usage of OpenGL ES 2.0 or higher on platforms that
    # use dynamic loading of the OpenGL implementation.

    if cfg.FAULT_HANDLER:
        faulthandler.enable(file=sys.stderr, all_threads=True)
    # if cfg.PROFILING_MODE:
    #     sys.setprofile(tracefunc)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL) #0226-
    initialize_user_preferences() # calls update_preferences_model()
    convert_projects_model()
    # configure_project_paths()
    # app = QApplication([])
    # app = QApplication(sys.argv)
    # app.setStyle('Fusion') | Fusion/Breeze/Oxygen/Windows
    cfg.mw = cfg.main_window = MainWindow()
    logger.info('Showing application window')
    cfg.mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print('__main__:')
    print('Configuring environment variables...')
    os.environ['PYTHONHASHSEED'] = '1'
    os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ["BLOSC_NTHREADS"] = '1'
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.5'
    os.environ['LIBTIFF_STRILE_ARRAY_MAX_RESIZE_COUNT'] = '1000000000'
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    # os.environ['QT_SCALE_FACTOR'] = '1' # scale the entire application
    # os.environ["QT_ENABLE_HIGHDPI_SCALING"] = '1'
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = '1'
    # os.environ["QT_DEBUG_PLUGINS"] = '1'
    # os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9000'
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-web-security --no-sandbox --num-raster-threads=%s ' \
                                               '--enable-logging --log-level=3' % \
                                              cfg.QTWEBENGINE_RASTER_THREADS
    print('Initializing QApplication...')
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Tahoma") #Consolas
    font.setPointSize(10)
    # font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    # font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    if is_mac():
        print(f"Dark Mode? {check_macos_isdark_theme()}")
    print('Entering main()...')
    main()