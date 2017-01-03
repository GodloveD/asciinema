from asciinema.commands.command import Command
from asciinema.editor import editor 
import asciinema.asciicast as asciicast


class EditCommand(Command):

    def __init__(self, infile, outfile, time_spec, clip):
        Command.__init__(self)
        self.infile = infile
        self.outfile = outfile
        self.time_spec = time_spec 
        self.clip = clip

    def execute(self, subfunction):
        try:
            self.editor.subfunction(asciicast.load(self.infile), self.time_spec, self.clip, self.outfile)

        except asciicast.LoadError as e:
            self.print_warning("Failed to load asciicast: %s" % str(e))
            return 1

        return 0
