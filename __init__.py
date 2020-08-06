import sys
import os
import re
from cudatext import *

if os.name=='nt':
    import pywin32
    from .simple_tts import tts_win as tts
else:
    raise RuntimeError("TextToSpeech currently only supports Windows")

fn_ini = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_texttospeech.ini')

op_rate = 1
op_volume = 100
op_voice = ''
debug_print = False
replace_eol = True

def bool_to_str(b):

    return '1' if b else '0'

def load_options():

    global op_rate
    global op_volume
    global op_voice
    global debug_print
    global replace_eol

    op_rate = int(ini_read(fn_ini, 'op', 'tts_rate', str(op_rate)))
    op_volume = int(ini_read(fn_ini, 'op', 'tts_volume', str(op_volume)))
    op_voice = ini_read(fn_ini, 'op', 'tts_voice', op_voice or '')
    if op_voice=='':
        op_voice = None
    debug_print = ini_read(fn_ini, 'op', 'debug_print', '0')=='1'
    replace_eol = ini_read(fn_ini, 'op', 'replace_eol', '1')=='1'

    if debug_print:
        print("TextToSpeech settings:")
        print("  rate:", op_rate)
        print("  volume:", op_volume)
        print("  voice:", op_voice)
        print("  replace_eol:", replace_eol)

def save_options():

    ini_write(fn_ini, 'op', 'tts_rate', str(op_rate))
    ini_write(fn_ini, 'op', 'tts_volume', str(op_volume))
    ini_write(fn_ini, 'op', 'tts_voice', op_voice or '')
    ini_write(fn_ini, 'op', 'debug_print', bool_to_str(debug_print))
    ini_write(fn_ini, 'op', 'replace_eol', bool_to_str(replace_eol))


def init_voice():

    try:
        return tts.reinitialize_voice(
            rate=op_rate,
            volume=op_volume,
            voice=op_voice,
        )
    except:
        pass


class Command:

    def __init__(self):
        
        load_options()
        init_voice()

    def do_speak(self):

        x, y, x1, y1 = ed.get_carets()[0]
        if y1<0:
            text = ed.get_text_all()
        else:
            text = ed.get_text_sel()
        if not text:
            print('No text to process')
            return

        if replace_eol:
            trivial_eol_newline_regex = re.compile(r"\n(?=\w)")  # Newline not followed by another newline.
            text, counts = trivial_eol_newline_regex.subn(" ", text)  # Replace trivial newlines in text with a space.
            if debug_print:
                print("Substituted %s trivial end-of-line newlines a space." % (counts, ))

        '''
        if regex_substitutions:
            for pattern, repl in regex_substitutions:
                text, counts = re.subn(pattern, repl, text)
                if debug_print:
                    print("Substituted %s instances of pattern %r with string %r:" % (counts, pattern, repl))
        '''

        if debug_print:
            print("tts.speak(<%s chars>) ..." % (len(text),), end="")
        ret = tts.speak(text)
        if debug_print:
            print(ret)


    def do_pause(self):

        if debug_print:
            print("tts.pause() ... ", end="")
        ret = tts.pause()
        if debug_print:
            print(ret)


    def do_resume(self):

        if debug_print:
            print("tts.resume() ... ", end="")
        ret = tts.resume()
        if debug_print:
            print(ret)


    def do_skip(self):

        if debug_print:
            print("tts.skip() ... ", end="")
        ret = tts.skip(num_skip=1)
        if debug_print:
            print(ret)


    def do_stop(self):

        if debug_print:
            print("tts.skip_all() ... ", end="")
        ret = tts.skip_all()
        if debug_print:
            print(ret)

    def reinit(self):

        if debug_print:
            print("tts.reinitialize_voice() ... ", end="")
        ret = init_voice()
        if debug_print:
            print(ret)

    def config(self):
        
        save_options()
        file_open(fn_ini)
