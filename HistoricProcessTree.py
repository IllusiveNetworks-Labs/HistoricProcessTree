"""
An Incident Response tool that visualizes historic process execution evidence (based on Event ID 4688 - Process Creation Event) in a tree view.
"""
import argparse
from process_create_event import EventCreatedProcesses

def main(args):
    processes_obj = EventCreatedProcesses(args.input_file, args.s, args.e, args.hours, args.output_file)
    processes_obj.getCreatedProcesses()
    processes_obj.generateHTML()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EVTX Parser for 4688 events. ')

    parser.add_argument('input_file', help='Path to evtx file')
    parser.add_argument('output_file', help='Name of the final html file')
    parser.add_argument('-s', help='Start date filter- Format: "MM/DD/YYYY HH:MM:SS" ')
    parser.add_argument('-e', help='End date filter- Format: "MM/DD/YYYY HH:MM:SS"')
    parser.add_argument('--hours', type=int, help='Hours to filter from the last event')
    args = parser.parse_args()

    exit(main(args))
  