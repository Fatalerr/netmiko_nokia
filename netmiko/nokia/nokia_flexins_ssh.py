"""Nokia FlexiNS/DX200 MML support."""
from __future__ import print_function
from __future__ import unicode_literals
import re
import time
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko.linux.linux_ssh import LinuxSSH

class NokiaFlexinsSSH(CiscoSSHConnection):
    """Nokia FlexiNS/DX200 MML support."""
    
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        self.RETURN = '\r\n'        
        self._test_channel_read()
        self.set_base_prompt()
        self.disable_paging()
        self.set_terminal_width()        

        
    def find_prompt(self, delay_factor=1):
        """Finds the current network device prompt, last line only.

        :param delay_factor: See __init__: global_delay_factor
        :type delay_factor: int
        """
        delay_factor = self.select_delay_factor(delay_factor)
        self.clear_buffer()
        self.write_channel(self.RETURN)
        time.sleep(delay_factor * 0.1)

        # Initial attempt to get prompt
        prompt = self.read_channel()
        #print("prompt:",[prompt])
        if self.ansi_escape_codes:
            prompt = self.strip_ansi_escape_codes(prompt)
            
        # Check if the only thing you received was a newline
        count = 0
        prompt = prompt.strip()
        while count <= 10 and not prompt:
            prompt = self.read_channel().strip()
            if prompt:
                if self.ansi_escape_codes:
                    prompt = self.strip_ansi_escape_codes(prompt).strip()
            else:
                self.write_channel(self.RETURN)
                time.sleep(delay_factor * 0.1)
            count += 1

        # If multiple lines in the output take the last line
        prompt = self.normalize_linefeeds(prompt)
        prompt = prompt.split(self.RESPONSE_RETURN)[-1]
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Unable to find prompt: {}".format(prompt))
        time.sleep(delay_factor * 0.1)
        self.clear_buffer()
        return prompt    
        
    def set_base_prompt(
        self, pri_prompt_terminator='< \x08', alt_prompt_terminator="<", delay_factor=1
    ):
        """Determine base prompt."""
        prompt = self.find_prompt(delay_factor=delay_factor)
        #print("prompt3:",[prompt],[pri_prompt_terminator])
        if not prompt in (pri_prompt_terminator, alt_prompt_terminator):
            raise ValueError("Router prompt not found: {0}".format(repr(prompt)))
        # Strip off trailing terminator
        self.base_prompt = prompt
        return self.base_prompt    

        
    def cleanup(self):
        """Try to Gracefully exit the SSH session."""
        self._session_log_fin = True
        self.write_channel("ZZZ;" + self.RETURN)