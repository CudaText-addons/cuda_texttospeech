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
    debug_print = ini_read(fn_ini, 'op', 'debug_print', '1')=='1'
    replace_eol = ini_read(fn_ini, 'op', 'replace_eol', '1')=='1'
    
    if debug_print:
        print("TextToSpeech settings:")
        print("rate:", op_rate)
        print("volume:", op_volume)
        print("voice:", op_voice)
    return tts.reinitialize_voice(
        rate=op_rate,
        volume=op_volume,
        voice=op_voice,
    )

load_options()


class Command:

    def do_speak(self):
        
        load_options()
        if debug_print: 
            print("\nTextToSpeech Speak, settings:")
            print("  debug_print: ", debug_print)
            print("  replace_eol: ", replace_eol)
            #print("  regex_substitutions: ", "".join("\n    - %s" % (tup,) for tup in regex_substitutions) if regex_substitutions else regex_substitutions)

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
        
        load_options()
        if debug_print:
            print("tts.pause() ... ", end="")
        ret = tts.pause()
        if debug_print:
            print(ret)


    def do_resume(self):
        
        load_options()
        if debug_print:
            print("tts.resume() ... ", end="")
        ret = tts.resume()
        if debug_print:
            print(ret)


    def do_skip(self, num_skip=1):
        
        load_options()
        if debug_print:
            print("tts.skip(%s) ... " % (num_skip,), end="")
        ret = tts.skip(num_skip=num_skip)
        if debug_print:
            print(ret)


    def do_stop(self):
        
        load_options()
        if debug_print:
            print("tts.skip_all() ... ", end="")
        ret = tts.skip_all()
        if debug_print:
            print(ret)

    def reinit(self):
        
        load_options()
        if debug_print:
            print("tts.reinitialize_voice() ... ", end="")
        ret = load_options()
        if debug_print:
            print(ret)
