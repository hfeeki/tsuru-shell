## {{{ http://code.activestate.com/recipes/280500/ (r1)
## console.py
## Author:   James Thiele
## Date:     27 April 2004
## Version:  1.0
## Location: http://www.eskimo.com/~jet/python/examples/cmd/
## Copyright (c) 2004, James Thiele

import os
import cmd
try:
    import readline
except:
    readline = None

from tsuruclient import apps   
from tsuruclient import auth

class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        if not readline :
            self.completekey = None
        self.prompt = "(tsuru)> "
        self.intro  = "Welcome to tsuru console!" ## defaults to None

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

DefaultTarget = "http://tsuru.plataformas.glb.com:8080"

class ITsuru(Console):

    def __init__(self):
        Console.__init__(self)
        self._get_target()
        self.intro  = "Welcome to tsuru console! Current target is: %s ." % self.target ## defaults to None

        self.apps = apps.AppManager(target)
        self.auth = auth.AuthManager(target)

    def _get_target(self):
        fn = os.path.join(os.getenv('HOME'), '.tsuru_target')
        if os.path.exists(fn):            
            with open(fn) as f:
                self.target = f.read().strip()
        else:
            self.target = DefaultTarget

    def do_target(self, arg):
        fn = os.path.join(os.getenv('HOME'), '.tsuru_target')
        if len(arg) < 1:
            self._get_target()            
        else:
            # write target
            target = arg.strip()
            with open(fn, 'w') as f:
                f.write(target)
            self.target = target
            print "Set target as %s success." % target
        print "Current target is: %s ." % self.target        

    def help_target(self):
        print "get or set target."

    def do_useradd(self, email):
        # check email is valid
        # create a user with email
        self.auth.create(email)




if __name__ == '__main__':
        console = ITsuru()
        console . cmdloop() 
## end of http://code.activestate.com/recipes/280500/ }}}
