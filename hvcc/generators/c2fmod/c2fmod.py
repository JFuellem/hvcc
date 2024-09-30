# Copyright (C) 2014-2018 Enzien Audio, Ltd.
# Copyright (C) 2021-2024 Wasted Audio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import time
from typing import Dict, Optional

from ..copyright import copyright_manager
from ..filters import filter_plugin_id


class c2fmod:
    """Generates a plugin wrapper for Firelights FMOD game audio middleware
    platform.
    """

    @classmethod
    def compile(
            cls,
            c_src_dir: str,
            out_dir: str,
            externs: Dict,
            patch_name: Optional[str] = None,
            patch_meta: Optional[Dict] = None,
            num_input_channels: int = 0,
            num_output_channels: int = 0,
            copyright: Optional[str] = None,
            verbose: Optional[bool] = False
    ) -> Dict:
        tick = time.time()
        
        out_dir = os.path.join(out_dir, "fmod")
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


        try:
            out_dir = os.path.abspath(out_dir)

            # copy over static files
            shutil.copytree(static_dir, out_dir, dirs_exist_ok=True)
            
            #ensure sourcefile folder of the wrapper is empty
            source_out_dir = os.path.join(out_dir, "SrcExportDir", "c")
            if os.path.exists(source_out_dir):
                shutil.rmtree(source_out_dir)
            
            # copy over generated C source files
            shutil.copytree(c_src_dir, source_out_dir)

            return {
                "stage": "c2fmod",
                "notifs": {
                    "has_error": False,
                    "exception": None,
                    "warnings": [],
                    "errors": []
                },
                "in_dir": c_src_dir,
                "in_file": "",
                "out_dir": out_dir,
                "out_file": "",
                "compile_time": time.time() - tick
            }

        except Exception as e:
            return {
                "stage": "c2fmod",
                "notifs": {
                    "has_error": True,
                    "exception": e,
                    "warnings": [],
                    "errors": [{
                        "enum": -1,
                        "message": str(e)
                    }]
                },
                "in_dir": c_src_dir,
                "in_file": "",
                "out_dir": out_dir,
                "out_file": "",
                "compile_time": time.time() - tick
            }
