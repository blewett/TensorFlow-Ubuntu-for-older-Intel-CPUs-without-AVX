"""
  section-shell.py: Original work Copyright (C) 2021 by Doug Blewett

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

def find_longest_section_name(content):
    max = 0
    print("sections:")
    for line in content:
        where = line.find(section_tag)
        if where == 0:
            print("  " + line)
            line = line[section_tag_len:].strip()
            where = line.find(":")
            section = line[:where].strip()
            length = len(section)
            if length > max:
                max = length
    return max

def main(filename, skip_section, skip_sub):
    content = read_content(sys.argv[1])
    if len(content) == 0:
        print(prog + ": the file " + sys.argv[1] + " has no content lines")
        exit(1)

    base_indent_len = find_longest_section_name(content)
    if base_indent_len == 0:
        print(prog + ": the file " + sys.argv[1] + " has no section entries")
        exit(1)

    base_indent = " " * base_indent_len

    # skip by default until the skip_section has been found
    skip = True
    execute = False
    section = ""
    clear_next_section = False
    sub = 0
    for line in content:
        # skip blank lines
        if len(line) == 0:
            continue

        # look for section headers at the front of the line
        where = line.find(section_tag)
        if where == 0:
            sub = 0
            line = line[section_tag_len:].strip()
            where = line.find(":")
            section = line[:where].strip()
            indent = " " * (base_indent_len - len(section))

            cd_string = ""
            where = line.find("DO CD ")
            if where > 0:
                cd_string = str(line[where + 6:])
                cd_string = cd_string.strip()

            # are we skipping sections
            if clear_next_section == True:
                skip_section = ""
                clear_next_section = False

            if skip_section != "":
                if skip_section != section:
                    print("* " + indent + line)
                    print("skipped")
                    continue

                clear_next_section = True

                if skip_sub > sub:
                    print("")
                    print("skipping until " +
                          str(section) + "." + str(skip_sub))
                else:
                    skip_section = ""

            execute = False
            skip = False
            while True:
                print("")
                print("* " + indent + line)
                text = input("    e(xecute), s(kip), q(uit)?")

                if text[0] == 'q':
                    exit(0)
                if text[0] == 'e' or text[0] == 'x':
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
                if text[0] == 's':
                    skip = True
                    break

                print("")

            continue

        if section == "":
            continue

        if line[0] != '#':
            sub += 1

        if skip == True:
            continue

        if skip_section != "" and skip_section != section:
            continue

        indent = " " * (base_indent_len - len(section)) + section
        if line[0] == '#':
            print("    " + base_indent + line)
            continue
        else:
            print(indent + "." + str(sub) + ": " + line)

        if skip_section != "":
            if sub >= skip_sub:
                skip_section = ""
            else:
                print("skipped")
                print("")
                continue

        if execute == True:
            print("")
            os.system(line)
            print("")
            continue

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
    print("     *  1: install python3 and build utilities")
    print("     e(xecute), s(kip), q(uit)?")
    print("")
    print("   The user may elect to execute or skip the shell commands in a section.")
    print("   There may be multiple commands in each section.  The commands are")
    print("   numbered as they are executed.")
    print("")
    print("   The arguments for section-shell.py are \"filename [section] [sub command #]\".")
    print("   The section and the sub number are optional and if provided will result in")
    print("   processing starting in the named section and at the sub number (shell")
    print("   command).")

#
# parse program argument
#
argc = len(sys.argv)
prog = sys.argv[0]

if (argc == 1 or argc > 4):
    print(prog + ": " + prog + " filename [section] [sub command #]")
    print(prog + ":   the first argument should be a filename.")
    exit(1)

filename = ""
section = ""
sub = 0

for arg in sys.argv:
    if arg == "?" or arg == "-?" or arg == "-h" or arg == "help":
        help(prog)
        exit(1)

if (argc >= 2):
    filename = sys.argv[1]

if (argc >= 3):
    section = sys.argv[2]

if (argc == 4):
    sub = sys.argv[3]
    if sub.isdigit() == False:
        print(prog + ": " + prog + " filename [section] [sub command #]")
        print(prog + ":   the sub command # must be a number.")
        exit(1)
    sub = int(sub)

main(filename, section, sub)

