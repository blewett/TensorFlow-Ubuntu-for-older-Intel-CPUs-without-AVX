"""
  section-shell.py: Original work Copyright (C) 2021 by Megan Blewett

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

  run shell files in sections

"""
import sys
import os

section_tag = "# section "
section_tag_len = 10

def read_content(file):
    try:
        with open(file) as f:
            content = f.readlines()
    except IOError:
        print(prog + ": could open the file: \"" + file + "\"")
        exit()

    f.close()
    content = [line.strip() for line in content]
    return content

def find_section_info(content):
    sections = []
    max = 0
    index = 0
    for line in content:
        where = line.find(section_tag)
        if where == 0:
            line = line[section_tag_len:].strip()
            where = line.find(":")
            section = line[:where].strip()
            sections.append([section,index])
            length = len(section)
            if length > max:
                max = length
        index += 1
    return max, sections

def list_content(content, sections):
    for sect in sections:
        print(content[sect[1]])

def main(filename, skip_section, skip_command_number):
    content = read_content(sys.argv[1])
    content_length = len(content)
    if content_length == 0:
        print(prog + ": the file " + sys.argv[1] + " has no content lines")
        exit(1)

    (base_indent_len,sections) = find_section_info(content)
    if len(sections) == 0:
        print(prog + ": the file " + sys.argv[1] + " has no section entries")
        exit(1)

    list_content(content, sections)
    print("")

    base_indent = " " * base_indent_len

    # skip by default until the skip_section has been found
    skip = True
    execute = False
    section = ""
    clear_next_section = False
    command_number = 0
    index = 0
    while index < content_length:
        #
        # process a line at a time
        #
        line = content[index]

        # skip blank lines
        if len(line) == 0:
            index += 1
            continue

        # look for section headers
        found_sect = None
        for sect in sections:
            if index == sect[1]:
                found_sect = sect
                break

        #
        # process a section header
        #
        if found_sect != None:
            command_number = 0
            section = sect[0]
            indent = " " * (base_indent_len - len(section))

            cd_string = ""
            where = line.find("DO CD ")
            if where > 0:
                cd_string = str(line[where + 6:])
                cd_string = cd_string.strip()

            # are we skipping sections
            if clear_next_section == True:
                skip_section = ""
                skip_command_number = 0
                clear_next_section = False

            if skip_section != "":
                if skip_section != section:
                    print(content[index])
                    print("skipped")
                    index += 1
                    continue

                clear_next_section = True

                if skip_command_number > command_number:
                    print("skipping until section " + str(section) +
                          " and command number " + str(skip_command_number))
                else:
                    skip_section = ""

            execute = False
            skip = False
            while True:
                print(content[index])
                text = input("    e(xecute), s(kip), l(list), j(jump), q(uit)?").strip()

                if text == 'q':
                    exit(0)

                if text == 'e' or text == 'x':
                    execute = True
                    if cd_string != "":
                        try:
                            os.chdir(cd_string)
                        except:
                            print("")
                            print("change directory to " + cd_string + " failed")
                            print("")

                    cd_string = ""
                    break

                if text == 's':
                    skip = True
                    break

                # jump
                txt = text.split(" ")
                if txt[0] == 'j':
                    length = len(txt)
                    if length < 2 or length > 3:
                        print("the jump command includes the section and the optional command number")
                        continue
                    # check the section
                    if length > 1:
                        found = False
                        for sect in sections:
                            if sect[0] == txt[1]:
                                section = sect[0]
                                skip_section = sect[0]
                                skip_command_number = 0
                                index = sect[1] - 1
                                found = True
                                break
                        if found == False:
                            print("the jump command section is not a section: " + txt[1])
                            continue
                            
                        # check the command_number
                        skip_command_number = 0
                        if length == 3:
                            if txt[2].isdigit() == False:
                                print("the jump command number must be an integer: " + txt[2])
                                continue;
                            skip_command_number = int(txt[2])

                        if skip_command_number < 1:
                            print("jumping to section " + skip_section)
                        else:
                            print("jumping to section " + skip_section +
                                  "  and command_number" + str(skip_command_number))
                        break

                # list
                if text == 'l':
                    list_content(content, sections)
                    continue

                print("")

            index += 1
            continue

        #
        # end of processing a section header
        #
        if section == "":
            index += 1
            continue

        if line[0] != '#':
            command_number += 1

        if skip == True:
            index += 1
            continue

        if skip_section != "" and skip_section != section:
            index += 1
            continue

        indent = " " * (base_indent_len - len(section)) + section
        if line[0] == '#':
            print(line)
            index += 1
            continue
        else:
            print(indent + "(" + str(command_number) + "): " + line)

        if skip_section != "":
            if command_number >= skip_command_number:
                skip_section = ""
            else:
                print("skipped")
                print("")
                index += 1
                continue

        if execute == True:
            os.system(line)
            print("")
            index += 1
            continue

        index += 1

    print("done")
# end of main

def help(prog):
    print("")
    print("  " + prog + ":")
    print("")
    print("   The benefit of \"section-shell.py\" is that it helps organize large")
    print("   and complex tasks that require user interaction.  The user provides")
    print("   a shell file containing all of the steps required for the task even")
    print("   though success in completing the task in a single run is unlikely.")
    print("   Sections can be easily repeated until the processing is complete.")
    print("")
    print("   This program runs sections of a named shell file.  The syntax of the ")
    print("   shell file is that of named sections.  The following line might be ")
    print("   used to start a section to perform installs")
    print("")
    print("     # section 1: install python3 and build utilities")
    print("     date")
    print("     touch timestamp")
    print("     make install")
    print("")
    print("   section-shell.py will display the following for that section:")
    print("")
    print("   # section 1: install python3 and build utilities")

    print("      e(xecute), s(kip), l(list), j(jump), q(uit)?")
    print("")
    print("   The user may elect to execute or skip the shell commands in a section.")
    print("   There may be multiple commands in each section.  The commands are")
    print("   numbered as they are executed.")
    print("")
    print("   The arguments for section-shell.py are \"filename [section] [command_number]\".")
    print("   The section and the command_number are optional and if provided will result")
    print("   in processing starting in the named section and at the command_number (shell")
    print("   command).")

#
# parse program argument
#
argc = len(sys.argv)
prog = sys.argv[0]

if (argc == 1 or argc > 4):
    print(prog + ": " + prog + " filename [section] [command_number]")
    print(prog + ":   the first argument should be a filename.")
    exit(1)

filename = ""
section = ""
command_number = 0

for arg in sys.argv:
    if arg == "?" or arg == "-?" or arg == "-h" or arg == "help":
        help(prog)
        exit(1)

if (argc >= 2):
    filename = sys.argv[1]

if (argc >= 3):
    section = sys.argv[2]

if (argc == 4):
    command_number_s = sys.argv[3]
    if command_number_s.isdigit() == False:
        print(prog + ": " + prog + " filename [section] [command_number]")
        print(prog + ":   the command_number must be a number.")
        exit(1)
    command_number = int(command_number_s)

main(filename, section, command_number)

