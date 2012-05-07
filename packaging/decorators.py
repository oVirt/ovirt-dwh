#!/usr/bin/python
'''
decorators for ovirt-engine-dwh-setup & ovirt-reports-setup
'''
import common_utils as utils
import sys
import logging
import traceback

def transactionDisplay(displayString):
    def wrap(f):
        def wrapped_f(*args):
            spaceLen = 70 - len(displayString)
            output = None
            try:
                print "%s..." % displayString,
                sys.stdout.flush()
                logging.debug("running %s" % f.func_name)
                if len(args) > 0:
                    output = f(*args)
                else:
                    output = f()
                print ("[ " + utils._getColoredText("DONE", utils.GREEN) + " ]").rjust(spaceLen -3)
                return output
            except Exception, (instance):
                print ("[ " + utils._getColoredText("ERROR", utils.RED) + " ]").rjust(spaceLen)
                logging.error(traceback.format_exc())
                raise Exception(instance)
        return wrapped_f
    return wrap
