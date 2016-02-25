#!/usr/bin/python -tt

# f = open(filename, 'r')

import sys
import os
import re
import SubnetTree

if len(sys.argv) < 2:
        sys.stderr.write('Usage: rc.py <filename>\nOutput: <file>.diff\n')
        sys.exit(1)
else:
        with open(sys.argv[1], 'r') as f:
            filename = os.path.splitext(sys.argv[1])[0]
            data = f.read()
            
def main():
    #sys.stdout = open(filename+'.diff', 'w')
    ospf_exp = re.compile('O .. .+?(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\/\d\d)')
    bgp_exp = re.compile('[s|\>|r|\*|i].+?(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\/\d{1,2})')
    # this RE match those prefixes without "/nn"
    # IOS do not append "/" for default mask eg /32 in 
    # 192.89.222.0/24 in BGP will appears as 192.89.222.0
    bgp_null_exp = re.compile('[\>|r|\*|i]+? +(\d{1,3}.\d{1,3}.\d{1,3}.0) ')
    ospf = ospf_exp.findall(data)
    bgp = bgp_exp.findall(data)
    bgp_null = bgp_null_exp.findall(data)

    # Build a BGP table (Tree)
    bgp_rib = SubnetTree.SubnetTree()
    for x in bgp: 
        if x != "0.0.0.0/0": bgp_rib.insert(x) 
    for x in bgp_null : 
        if x != "0.0.0.0/0": bgp_rib.insert(x) 
  
    # Check all OSPF prefixes to see if it's in BGP rib
    # Test the prefix and isert the result into the 
    # OSPF present database
    ospf_present = { x: x in bgp_rib for x in ospf }

    for x in ospf_present: 
        # Only print the missing OSPF if the input is false
        if (ospf_present[x] == False):
            print x,": Missing in BGP"

if __name__ == '__main__':
  main()

