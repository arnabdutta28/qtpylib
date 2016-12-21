#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AsyncPy: Simple Async
# https://github.com/ranaroussi/qtpylib
#
# Copyright 2016 Ran Aroussi
#
# Licensed under the GNU Lesser General Public License, v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from threading import Thread
from time import sleep, time

# =============================================
class RecurringTask(Thread):
    """Calls a function at a sepecified interval."""
    def __init__(self, func, interval_sec, init_sec=0, *args, **kwargs):
        """Call `func` every `interval_sec` seconds.

        Starts the timer.

        Accounts for the runtime of `func` to make intervals as close to `interval_sec` as possible.
        args and kwargs are passed to Thread().

        :Parameters:
            func : object
                Function to invoke every N seconds
            interval_sec : int
                Call func every this many seconds
            init_sec : int
                Wait this many seconds initially before the first call
            *args : mixed
                parameters sent to parent Thread class
            **kwargs : mixed
                parameters sent to parent Thread class
        """

        # threading.Thread.__init__(self, *args, **kwargs) # For some reason super() doesn't work
        super().__init__(*args, **kwargs) # Works!
        self._func        = func
        self.interval_sec = interval_sec
        self.init_sec     = init_sec
        self._running     = True
        self._functime    = None # Time the next call should be made

        self.start()

    def __repr__(self):
        return 'RecurringTask({}, {}, {})'.format(self._func, self.interval_sec, self.init_sec)

    def run(self):
        """Start the recurring task."""
        if self.init_sec:
            sleep(self.init_sec)
        self._functime = time()
        while self._running:
            start = time()
            self._func()
            self._functime += self.interval_sec
            if self._functime - start > 0:
                sleep(self._functime - start)

    def stop(self):
        """Stop the recurring task."""
        self._running = False

