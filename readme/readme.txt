Plugin for CudaText.
Uses system-provided speech synthesis platform to speak text.
Windows only (yet), the "SAPI" speech engine/platform is used.
Requires additional package "pywin32", from CudaText addons.

Speaks selected text, or entire document if nothing selected.

Plugin has config file, to call it: "Options / Settings-plugins / TextToSpeech".

Currently (Win10 x64 2004) only empty "voice" option works, changing it to
"Microsoft Sam" or "Microsoft David" gives exception in SAPI library.

Ported from Sublime Text plugin "TextToSpeech".
Author: Alexey Torgashin (CudaText)
License: MIT
