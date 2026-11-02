"""Karan's desktop entry point. Reference demo works before teammates finish."""
import argparse
import os
import sys

def main() -> int:
    parser=argparse.ArgumentParser(description='CommunityScope desktop')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--team',action='store_true',help='Require teammates core/ modules')
    group.add_argument('--demo',action='store_true',help='Use separately labelled reference backend')
    args=parser.parse_args()
    if args.team:os.environ['COMMUNITYSCOPE_BACKEND']='team'
    elif args.demo:os.environ['COMMUNITYSCOPE_BACKEND']='reference'
    from PySide6.QtWidgets import QApplication,QMessageBox
    app=QApplication(sys.argv[:1]);app.setApplicationName('CommunityScope')
    try:
        from gui.main_window import MainWindow
        window=MainWindow()
    except Exception as exc:
        import traceback
        details=traceback.format_exc();print(details,file=sys.stderr)
        box=QMessageBox();box.setWindowTitle('CommunityScope setup error')
        box.setText(str(exc));box.setDetailedText(details);box.exec();return 1
    window.show();return app.exec()

if __name__=='__main__':sys.exit(main())
