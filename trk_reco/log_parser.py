import pandas as pd
import re

class Info(object):
    def __init__(self, start_str, end_str, delaystart=0):
        self.start = False
        self.saved = False
        self.start_str = start_str
        self.end_str = end_str
        self.delay_start = delaystart

    def parse(self, line):
        if self.start_str in line[:len(self.start_str)]:
            if self.saved and not self.start:
                # if info has been saved, this could be a false start-signal
                return

            self.start = True

        if self.start and self.delay_start > 0:
            self.delay_start -= 1
            # delay the start
            return

        if self.end_str == line[:len(self.end_str)]:
            self.start = False

        if self.start:
            self.add(line)
            self.saved = True

    def add(self, line):
        pass

    def out(self):
        pass


class Timing(Info):
    def __init__(self):
        super().__init__('*****Chrono*****', 'ChronoStatSvc    ', delaystart=2)

        self.tool_list_l = []
        self.total_l = []
        self.avg_l = []
        self.min_l = []
        self.max_l = []
        self.evts_1 = []

    @classmethod
    def get_time_scale(self, unit):
        if "us" in unit:
            time_scale = 1e-6
        elif 'ms' in unit:
            time_scale = 1e-3
        elif 'min' in unit:
            time_scale = 60
        elif 's' in unit:
            time_scale = 1
        else:
            time_scale = -1
        return time_scale

    def add(self, line):
        has_avg = "Ave/Min/Max" in line
        items = line[:-1].split()

        tool_name = items[0]
        # don't perform replacement on the toolName
        new_str = " ".join(items[1:])
        new_str = new_str.replace('=', ' = ')
        new_str = new_str.replace('/', ' / ')
        new_str = new_str.replace('(', ' ( ')
        new_str = new_str.replace(')', ' ) ')
        new_str = new_str.replace('[', ' [ ')
        new_str = new_str.replace('+-', ' +- ')
        items = [items[0]] + new_str.split()

        try:
            time_unit = items[9]
        except IndexError:
            print(line)
            return

        time_scale = self.get_time_scale(items[9])
        if time_scale < 0:
            print("Time error0:", items)

        try:
            total_ = float(items[7])*time_scale
        except:
            total_ = 0
            print("Total ERROR:", items)

        evts_input_index = 12
        if has_avg:
            evts_input_index = 29

            try:
                time_unit = items[26]
            except IndexError:
                print("Time ERROR1:", items)
                return

            time_scale = self.get_time_scale(time_unit)
            if time_scale < 0:
                print("Time ERROR2", items)

            avg_ = float(items[16])*time_scale
            min_ = float(items[22])*time_scale
            max_ = float(items[24])*time_scale
        else:
            avg_ = min_ = max_ = -999

        try:
            evts_ = int(items[evts_input_index])
        except:
            evts_ = 0
            print("Evt ERROR", items)

        self.tool_list_l.append(tool_name)
        self.total_l.append(total_)
        self.avg_l.append(avg_)
        self.min_l.append(min_)
        self.max_l.append(max_)
        self.evts_1.append(evts_)

    def to_str(self):
        print(len(self.tool_list_l), len(self.total_l))

    def out(self):
        data = {
            "Tool":  self.tool_list_l,
            "Total": self.total_l,
            "Ave":   self.avg_l,
            "Min":   self.min_l,
            "Max":   self.max_l,
            "Nevt":  self.evts_1
        }
        df = pd.DataFrame(data)
        return df


class Match(object):
    def __init__(self, pattern):
        self.pp = re.compile(pattern)
        self.out_str = ""

    def parse(self, line):
        if self.pp.match(line):
            self.out_str += line

    def out(self):
        return self.out_str
