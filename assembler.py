#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
# Preprocess input file
def preprocess(lines):
    '''Skip whitespace'''
    while '\n' in lines: 
        lines.remove('\n')
    '''Skip comments '''
    comment = '//'
    crude = [item for item in lines if not(item.startswith(comment))]
    for n,i in enumerate(crude):
        c = i.find(comment)
        if c == -1:
            if i.endswith('\n'):
                crude[n] = i[:len(i)-1]
        else:
            crude[n] = i[:c]
    commands = [item.strip(' ') for item in crude]
    return commands
# Reading and parsing input file
def parser(inputf,outputf):
    #with open(filename) as f:
    inpt = open(inputf)
    lines = inpt.readlines()
    commands = preprocess(lines)
    out = open(outputf,'w')
    symbol_table = symbol_handle(commands)
    bi_value = ''
    for command in commands:
        if command_type(command) != 'L':
            if command_type(command) == 'A':
                p = command[1:]
                if not(p.isdigit()):
                    if p in symbol_table:
                        value = symbol_table[p]
                    elif p in predefined_table:
                        value = predefined_table[p]
                else:
                    value = int(p)
                bi_value = "{0:016b}".format(value)
            elif command_type(command) =='C':
                fields = field(command)
                bi_value = biconvertforC(fields)
            out.write(bi_value+'\n')
    inpt.close()
    out.close()
            
            
    
'''Detect command type'''
def command_type(command):
    if command.startswith('@'):
        return 'A' # A-Command
    if command.startswith('('):
        return 'L' # Label
    else:
        return 'C' # C-Command
        
'''Recognize fields (dest, comp, jump) from C-Command'''
def field(command):
    fields={}
    equal_pos = command.find('=')
    semicol_pos = command.find(';')
    if equal_pos == -1 and semicol_pos == -1:
        fields['comp']=command
        fields['dest']='null'
        fields['jump']='null'
    elif equal_pos == -1 and semicol_pos != -1:
        fields['jump']=command[semicol_pos+1:]
        fields['comp']=command[0:semicol_pos]
        fields['dest']='null'
    else:
        fields['dest']=command[0:equal_pos]
        if semicol_pos == -1:
            fields['comp']=command[equal_pos+1:]
            fields['jump']='null'
        else: 
            fields['jump']=command[semicol_pos+1:]
            fields['comp']=command[equal_pos+1:semicol_pos]
    return fields
# Converting mnemonics to code
comp_table = {'0':'0101010',
              '1':'0111111',
              '-1':'0111010',
              'D':'0001100',
              'A':'0110000',
              'M':'1110000',
              '!D':'0001101',
              '!A':'0110001',
              '!M':'1110001',
              '-D':'0001111',
              '-A':'0110011',
              '-M':'1110011',
              'D+1':'0011111',
              'A+1':'0110111',
              'M+1':'1110111',
              'D-1':'0001110',
              'A-1':'0110010',
              'M-1':'1110010',
              'D+A':'0000010',
              'D+M':'1000010',
              'D-A':'0010011',
              'D-M':'1010011',
              'A-D':'0000111',
              'M-D':'1000111',
              'D&A':'0000000',
              'D&M':'1000000',
              'D|A':'0010101',
              'D|M':'1010101'}
dest_table = {'null':'000',
              'M':'001',
              'D':'010',
              'MD':'011',
              'A':'100',
              'AM':'101',
              'AD':'110',
              'AMD':'111'}
jump_table = {'null':'000',
              'JGT':'001',
              'JEQ':'010',
              'JGE':'011',
              'JLT':'100',
              'JNE':'101',
              'JLE':'110',
              'JMP':'111'}
def biconvertforC(fields): #fields has to be a dict
    c=fields['comp']
    d=fields['dest']
    j=fields['jump']
    cc=comp_table[c]
    dd=dest_table[d]
    jj=jump_table[j]
    return '111'+cc+dd+jj
    
# Handling symbols
predefined_table = {'R0':0,
                    'R1':1,
                    'R2':2,
                    'R3':3,
                    'R4':4,
                    'R5':5,
                    'R6':6,
                    'R7':7,
                    'R8':8,
                    'R9':9,
                    'R10':10,
                    'R11':11,
                    'R12':12,
                    'R13':13,
                    'R14':14,
                    'R15':15,
                    'SP':0,
                    'LCL':1,
                    'ARG':2,
                    'THIS':3,
                    'THAT':4,
                    'SCREEN':16384,
                    'KBD':24576}

def symbol_handle(commands):
    '''Put label symbols in a symbol table'''
    symbol_table = {}
    count = 0
    for command in commands:
        if command_type(command) == 'L':
            label_tag = command[1:len(command)-1]
            val = commands.index(command)
            symbol_table[label_tag] = val-count 
            count += 1
            
    initial = 16
    for command in commands:
        if command_type(command) == 'A':
            a = command[1:len(command)]
            if not(a.isdigit()):
                if not(a in predefined_table or a in symbol_table) :
                    symbol_table[a]=initial
                    initial += 1
    return symbol_table
def main():
    inputf = "source_code.txt"
    outputf = "Prog.hack"
    #inputf = sys.argv[1]
    #outputf = sys.argv[2]
    parser(inputf,outputf)
    
if __name__ == "__main__":
    main()
  
                    
    
    
            