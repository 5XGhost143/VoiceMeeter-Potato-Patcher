import json
import pymem
import pymem.process
import sys
import os

class VoiceMeeterPatcher:
    def __init__(self):
        self.config = None
        self.load_config()
    
    def resource_path(self, relative_path):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def load_config(self):
        config_path = self.resource_path("config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file '{config_path}' not found!")
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except json.JSONDecodeError:
            raise Exception("Invalid JSON in config file!")
        
        required_keys = ["process_name", "module_name", "offsets"]
        for key in required_keys:
            if key not in self.config:
                raise KeyError(f"Missing key in config: {key}")
        
        offsets_keys = ["base_offset", "addr_offset"]
        for key in offsets_keys:
            if key not in self.config["offsets"]:
                raise KeyError(f"Missing offset key in config: {key}")
        
        return True
    
    def check_status(self):
        try:
            pm = pymem.Pymem(self.config["process_name"])
            module = pymem.process.module_from_name(pm.process_handle, self.config["module_name"]).lpBaseOfDll
            
            base_offset = int(self.config["offsets"]["base_offset"], 16)
            addr_offset = int(self.config["offsets"]["addr_offset"], 16)
            
            base = module + base_offset
            first_ptr = pm.read_uint(base)
            
            if first_ptr < 0x10000 or first_ptr > 0x7FFFFFFF:
                raise ValueError(f"Invalid pointer: {hex(first_ptr)}")
            
            final_addr = first_ptr + addr_offset
            
            if final_addr < 0x10000 or final_addr > 0x7FFFFFFF:
                raise ValueError(f"Invalid final address: {hex(final_addr)}")
            
            current_value = pm.read_uint(final_addr)
            
            return str(current_value).startswith("429496")
            
        except pymem.exception.ProcessNotFound:
            raise Exception(f"Process '{self.config['process_name']}' not found!\nMake sure VoiceMeeter Potato is running.")
    
    def apply_patch(self):
        try:
            pm = pymem.Pymem(self.config["process_name"])
            module = pymem.process.module_from_name(pm.process_handle, self.config["module_name"]).lpBaseOfDll
            
            base_offset = int(self.config["offsets"]["base_offset"], 16)
            addr_offset = int(self.config["offsets"]["addr_offset"], 16)
            
            base = module + base_offset
            first_ptr = pm.read_uint(base)
            
            if first_ptr < 0x10000 or first_ptr > 0x7FFFFFFF:
                raise ValueError(f"Invalid pointer: {hex(first_ptr)}")
            
            final_addr = first_ptr + addr_offset
            
            if final_addr < 0x10000 or final_addr > 0x7FFFFFFF:
                raise ValueError(f"Invalid final address: {hex(final_addr)}")
            
            current_value = pm.read_uint(final_addr)
            
            if str(current_value).startswith("429496"):
                return "already_patched"
            else:
                pm.write_int(final_addr, 0)
                return "success"
                
        except pymem.exception.ProcessNotFound:
            raise Exception(f"Process '{self.config['process_name']}' not found!\nMake sure VoiceMeeter Potato is running.")
    
    def get_process_name(self):
        return self.config.get("process_name", "Unknown") if self.config else "Unknown"
    
    def get_module_name(self):
        return self.config.get("module_name", "Unknown") if self.config else "Unknown"