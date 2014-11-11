# -*- coding: utf-8 -*-
import re
import subprocess
import os
import threading
from zipfile import ZipFile
import mmap

from scipy import signal

from LabFeiApplication.models import CorrectionErrors


__author__ = 'wachs'


def run_popen_with_timeout(command_string, timeout, input_data=None):
    """
    Run a sub-program in subprocess.Popen, pass it the input_data,
    kill it if the specified timeout has passed.
    returns a tuple of success, stdout, stderr
    """
    kill_check = threading.Event()

    def _kill_process_after_a_timeout(pid):
        os.kill(pid, signal.SIGTERM)
        kill_check.set()  # tell the main routine that we had to kill
        # use SIGKILL if hard to kill...
        return

    p = subprocess.Popen(command_string, bufsize=1, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = p.pid
    watchdog = threading.Timer(timeout, _kill_process_after_a_timeout, args=(pid, ))
    watchdog.start()
    (stdout, stderr) = p.communicate(input_data)
    watchdog.cancel()  # if it's still waiting to run
    success = not kill_check.isSet()
    kill_check.clear()
    return (success, stdout, stderr)


class Compiler():
    def __init__(self, file_list, output_filename):
        self.file_list = file_list
        self.output_filename = output_filename
        self.errors_list = []
        self.warnings_list = []
        self.compiler_output = ""

    def compile(self):

        process = subprocess.Popen("gcc -std=c89 -I./includes/ %s -o %s" % (" ".join(self.file_list), self.output_filename),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        (out, err) = process.communicate()
        process.wait()
        self.treat_stdout(out)
        self.treat_stderr(err)

    @staticmethod
    def split_errors(full_string):
        lines = full_string.split("\n")
        ret = []
        while len(lines) > 2:
            l = lines.pop(0) + "\n"
            while (lines[0][0] != '/' or lines[0].startswith("In file included")) and len(lines) > 2:
                l += lines.pop(0) + "\n"
            ret.append(l)
        return ret

    def treat_stdout(self, stdout):
        self.compiler_output = stdout

    def treat_stderr(self, stderr):
        errlist = Compiler.split_errors(stderr)
        self.errors_list = [l for l in errlist if (" error:" in l or " Undefined")]
        self.warnings_list = [l for l in errlist if (" warning:" in l)]


class CodeCorrector(object):
    def __init__(self, folder):
        self.folder = folder
        self.source_c = [folder + f for f in os.listdir(self.folder) if ("." in f and f.split(".")[1] == 'c')]
        self.exe_output = self.folder + "executable"
        self.warnings = []
        self.errors = []
        self.final_result = 0

    def before_correction(self):
        pass

    def run_correction(self):
        self.before_correction()
        compiler = Compiler(self.source_c, self.exe_output)
        compiler.compile()
        self.warnings = compiler.warnings_list
        self.errors = compiler.errors_list
        self.after_correction()

    def after_correction(self):
        pass


class ProgramRunner(object):
    def __init__(self):
        self.stderr = None
        self.stdout = None
        self.messages = []
        self.result = None
        self.success = 0

    def run(self, command, input=None, timeout=4000):
        # sub = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (sucess, stdout, stderr) = sub = run_popen_with_timeout(command, timeout, input)
        self.stdout = stdout
        self.stderr = stderr
        self.success = sucess
        self.parse_output()

    def parse_output(self):
        result = re.search("======result======\n(.*?)\n====end=result====", self.stdout, re.M)
        if result:
            self.result = float(result.group(1))

        messages_re = re.finditer("======message======.(.*?).====end=message====.", self.stdout, re.S | re.M)
        for reg in messages_re:
            print reg.group(1)
            self.messages.append(reg.group(1))


class CodeCorrectorMainReplacement(CodeCorrector):
    def __init__(self, folder, replacement_text):
        super(CodeCorrectorMainReplacement, self).__init__(folder)
        self.replacement_text = replacement_text
        self.messages = []
        self.final_result = 0
        self.success = 0


    def before_correction(self):
        print "fui chamado"
        source_main = self.find_main()
        self.replace_main(source_main)

    def after_correction(self):
        runner = ProgramRunner()
        runner.run(self.exe_output)
        self.success = runner.success
        self.messages = runner.messages
        self.final_result = runner.result

    def replace_main(self, source_main):

        with open(source_main, 'r') as f:
            code = f.read()

        code = "#include <corrector.h>\n" + code
        main_part = re.search("(.*?main *?\(.*?\).*?\{)(.*)\}", code, re.M | re.S).group(2)
        code = code.replace(main_part, "\n" + self.replacement_text + "\n")

        with open(source_main, 'w') as f:
            f.write(code)

    def find_main(self):
        found_main = None
        for source in self.source_c:
            size = os.stat(source).st_size
            f = open(source)
            data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
            m = re.search(".*?main *?\(.*?\).*?\{", data, re.M | re.S)
            if m:
                if found_main is not None:
                    raise Exception("Found 2 main files")
                else:
                    found_main = source

        return source


def start_correction(submission):
    zipped_file = submission.zippedFile
    z = ZipFile(zipped_file)
    output_folder = zipped_file.split(".")[0] + "/"
    z.extractall(output_folder)

    submission.status = "Corrigindo..."
    submission.save()

    if submission.laboratory.replaceMain:
        corrector = CodeCorrectorMainReplacement(output_folder, submission.laboratory.mainReplacement)
        corrector.run_correction()

    for err in corrector.errors:
        cerror = CorrectionErrors()
        cerror.laboratorySubmission = submission
        cerror.description = err
        cerror.type = "ERROR"
        cerror.save()

    for warn in corrector.warnings:
        cwarn = CorrectionErrors()
        cwarn.laboratorySubmission = submission
        cwarn.description = warn
        cwarn.type = "WARNING"
        cwarn.save()

    for msg in corrector.messages:
        cmsg = CorrectionErrors()
        cmsg.laboratorySubmission = submission
        cmsg.description = msg
        cmsg.type = "CORRECTION"
        cmsg.save()

    if len(corrector.errors) > 0:
        submission.status = "Não Compilou"
    elif len(corrector.warnings) > 0:
        submission.status = "Compilou com Warning"
    elif corrector.success is False or corrector.final_result < 10:
        submission.status = "Compilou e não executou"
    else:
        submission.status = "Compilou e executou"

    submission.grade = corrector.final_result
    submission.save()



