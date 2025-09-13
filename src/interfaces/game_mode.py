#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

class IGameMode(ABC):
    @property
    @abstractmethod
    def mode(self) -> int:
        pass
    
    @property
    @abstractmethod
    def list_movements(self) -> list[int]:
        pass
    
    @abstractmethod
    def reset_variables_mode(self):
        pass
        
    @abstractmethod
    def start(self, width: int, height: int):
        pass
    
    @abstractmethod
    def show_movement(self):
        pass
    
    @abstractmethod
    def show_repeat_msg(self):
        pass        
   