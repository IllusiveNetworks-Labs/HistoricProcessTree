import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile

import xmltodict
import jinja2
from anytree import search
from anytree.exporter import JsonExporter

from new_node import NewNode

TREE_HTML = "process_tree.html.j2"


class EventCreatedProcesses(object):
    def __init__(self, in_file, start_time, end_time, hours_from_last_event, output_file):
        self.output_file = output_file
        with NamedTemporaryFile(delete=False) as temp_file:
            tmp_name = temp_file.name

        print "Processing..."
        time_filter_string = ''
        if hours_from_last_event:
            time_filter_string = "StartTime=(get-winevent -FilterHashtable @{Path='%s';id=4688}  -MaxEvents 1 |" \
                                 " Select-Object TimeCreated).TimeCreated.AddHours(-%d)" % (in_file, hours_from_last_event)
        else :
            if start_time is not None:
                time_filter_string = "StartTime=get-date '%s'" % (start_time)
            if end_time is not None:
                time_filter_string += ";EndTime=get-date '%s'" % (end_time)
        command = "Get-WinEvent -FilterHashtable @{Path='%s';id=4688;%s} |" \
                  " Select-Object TimeCreated,Message | Export-Clixml %s" % (in_file, time_filter_string, tmp_name)
        subprocess.check_call(["powershell",command])

        with open(tmp_name) as mytemp:
            a = xmltodict.parse(mytemp.read())
        self.file_content = a['Objs']['Obj']

    # in order to make datetime serialzable
    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def event_date_to_datetime(self, date_string):
        return datetime.strptime(date_string[:23], '%Y-%m-%dT%H:%M:%S.%f' )

    def get_item(self, data_to_find, item_name):
        pos = data_to_find.index(item_name)
        end = data_to_find.find("_x000D", pos)
        newStr = data_to_find[pos:end].replace("_x0009_", "")
        item = newStr[newStr.find(":")+1:]
        return item

    def sort_events(self):
        relevant_events_info = []

        for item in reversed(self.file_content):
            event_date = self.event_date_to_datetime(item.get('MS').get('DT').get("#text"))
            xmldata = item.get('MS').get('S')['#text']
            pid = int(self.get_item(xmldata, "New Process ID"), 16)
            ppid = int(self.get_item(xmldata, "Creator Process ID"), 16)
            parentProcessName = self.get_item(xmldata, "Creator Process Name")
            processName = self.get_item(xmldata, "New Process Name")
            commandLine = self.get_item(xmldata, "Process Command Line")

            event_items = [pid, ppid, processName, commandLine, event_date, parentProcessName]
            relevant_events_info.append(event_items)

        return relevant_events_info

    def setNodeInfo(self, node, command_line, process_name, pid, event_date, parent_process_name):
        node.command_line = command_line
        node.text = process_name
        node.tags.append(str(pid))
        node.time = event_date
        node.parent_process_name = parent_process_name

    def getCreatedProcesses(self):
        main_node = NewNode(00000)
        main_node.text = "Event log Processes"
        relevant_events = self.sort_events()
        print "Num of events - " + str(len(relevant_events))
        for event_item in relevant_events:
            pid, ppid, new_process_name, command_line, event_date, parent_process_name = event_item[0], event_item[1], event_item[2], event_item[3], event_item[4],  event_item[5]

            # find if there is already a node of the parent id
            res = search.findall(main_node, filter_ = lambda node: node.name == ppid)
            if len(res) == 0:
                parent_node = NewNode(ppid, parent=main_node)
                parent_node.tags.append(str(ppid))
                parent_node.text = parent_process_name
                child_node = NewNode(pid, parent=parent_node)
                self.setNodeInfo(child_node, command_line, new_process_name, pid, event_date, parent_process_name)
            else:
                for parent_node in res:
                    child_node = NewNode(pid, parent=parent_node)
                    self.setNodeInfo(child_node, command_line, new_process_name, pid, event_date, parent_process_name)
                    if len(res) > 1:
                        child_node.unknown = True
                        child_node.text = "?" + new_process_name

        exporter = JsonExporter(indent=2,default = self.myconverter)
        d = exporter.export(main_node)

        # for bootstrap-treeview.js
        d2 = d.replace("children", "nodes")
        self.data = "[" + d2 + "]"

    def generateHTML(self):
        print "Generating HTML file - %s " % (self.output_file)
        new_data = jinja2.Environment(
            # load the template from working directory
            loader=jinja2.FileSystemLoader('.'),
            # Fail if there some jinja placeholders don't have values.
            undefined=jinja2.StrictUndefined
        ).get_template(TREE_HTML).render(my_data=self.data)

        with open(self.output_file, "w") as result_page:
            result_page.write(new_data)
        print "Done."